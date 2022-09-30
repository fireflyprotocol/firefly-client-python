from inspect import signature

from requests import delete
from api_service import APIService
from order_signer import OrderSigner
from onboarding_signer import OnboardingSigner
from utils import *
from enums import ORDER_SIDE, ORDER_TYPE
from constants import ADDRESSES,TIME, SERVICE_URLS
from interfaces import *
from enums import MARKET_SYMBOLS
from eth_account import Account


class FireflyClient:
    def __init__(self, are_terms_accepted, network, private_key, user_onboarding=True):
        self.are_terms_accepted = are_terms_accepted;
        self.network = network
        self.account = Account.from_key(private_key)
        self.apis = APIService(self.network["apiGateway"])
        self.order_signers = {};
        self.contracts = self.get_contract_addresses()
        self.onboarding_signer = OnboardingSigner(self.network["chainId"])
        # todo fetch from api
        self.default_leverage = 3

        if user_onboarding:
            self.apis.auth_token = self.onboard_user()

    def onboard_user(self, token:str=None):
        user_auth_token = token
        
        # if no auth token provided create on
        if not user_auth_token:
            message = OnboardingMessage(
            action=ONBOARDING_MESSAGES.ONBOARDING.value,
            onlySignOn=self.network["onboardingUrl"]
            )

            # sign onboarding message
            signed_hash = self.onboarding_signer.sign_msg(message, self.account.key.hex())

            response = self.authorize_signed_hash(signed_hash);

            if 'error' in response:
                raise SystemError("Authorization error: {}".format(response['error']['message']))

            user_auth_token = response['token']

        return user_auth_token

    def authorize_signed_hash(self, signed_hash:str):
        return self.apis.post(
            SERVICE_URLS["USER"]["AUTHORIZE"],
            {
                "signature": signed_hash,
                "userAddress": self.account.address,
                "isTermAccepted": self.are_terms_accepted,
            })

    def add_market(self, symbol: MARKET_SYMBOLS, orders_contract=None):
        symbol_str = symbol.value
        # if signer for market already exists return false
        if (symbol_str in self.order_signers):
            return False;



        # if orders contract address is not provided get 
        # from addresses retrieved from dapi
        if orders_contract == None:
            try:
                orders_contract = self.contracts[symbol_str]["Orders"]
            except:
                raise SystemError("Can't find orders contract address for market: {}".format(symbol_str))


        self.order_signers[symbol_str] = OrderSigner(
            self.network["chainId"],
            orders_contract
            )

        return True;

    def create_order_to_sign(self, params:OrderSignatureRequest):
        expiration = current_unix_timestamp()        
        # MARKET ORDER - set expiration of 1 minute
        if (params["orderType"] == ORDER_TYPE.MARKET):
            expiration += TIME["SECONDS_IN_A_MINUTE"]
        # LIMIT ORDER - set expiration of 30 days
        else:
            expiration += TIME["SECONDS_IN_A_MONTH"];

        return Order (
            isBuy = params["side"] == ORDER_SIDE.BUY,
            price = to_bn(params["price"]),
            quantity =  to_bn(params["quantity"]),
            leverage =  to_bn(default_value(params, "leverage", self.default_leverage)),
            maker =  self.account.address.lower(),
            reduceOnly =  default_value(params, "reduceOnly", False),
            triggerPrice =  to_bn(0),
            taker =  ADDRESSES["ZERO"],
            expiration =  default_value(params, "expiration", expiration),
            salt =  default_value(params, "salt", random_number(1000000)),
            )

    def create_signed_order(self, params:OrderSignatureRequest):
        """
        Used to create an order from provided params and sign it using the private
        key of the account

        Args:
            params (OrderSignatureRequest): parameters to create order with
 
        Returns:
            OrderSignatureResponse: order raw info and generated signature
        """
        
        # from params create order to sign
        order = self.create_order_to_sign(params)

        symbol = params["symbol"].value
        order_signer = self.order_signers.get(symbol);

        if not order_signer:
            raise SystemError("Provided Market Symbol({}) is not added to client library".format(symbol))
        
        order_signature = order_signer.sign_order(order, self.account.key.hex())
        
        return OrderSignatureResponse(
            symbol=symbol,
            price=params["price"],
            quantity=params["quantity"],
            side=params["side"],
            leverage=default_value(params, "leverage", self.default_leverage),
            reduceOnly=default_value(params, "reduceOnly", False),
            salt=order["salt"],
            expiration=order["expiration"],
            orderSignature=order_signature,
            orderType=params["orderType"],
        )
    
    def create_signed_cancel_order(self,params:OrderSignatureRequest):
        try:
            signer:OrderSigner = self.get_order_signer(params["symbol"])
            order_to_sign = self.create_order_to_sign(params)
            hash = signer.get_order_hash(order_to_sign)
            return self.create_signed_cancel_orders(params["symbol"],hash)
        except Exception as e:
            return ""

    def create_signed_cancel_orders(self,symbol:MARKET_SYMBOLS,order_hash:list):
        if type(order_hash)!=list:
            order_hash = [order_hash]
        order_signer:OrderSigner = self.get_order_signer(symbol)
        cancel_hash = order_signer.sign_cancellation_hash(order_hash)
        hash_sig = order_signer.sign_hash(cancel_hash,self.account.key.hex())
        return OrderCancellationRequest(
            symbol=symbol.value,
            hashes=order_hash,
            signature=hash_sig
        )

    def post_cancel_order(self,params:OrderCancellationRequest):
        return self.apis.delete(
            SERVICE_URLS["ORDERS"]["ORDERS_HASH"],
            {
            "symbol": params["symbol"],
            "orderHashes":params["hashes"],
            "cancelSignature":params["signature"]
            },
            auth_required=True
            )
    
    def post_signed_order(self, params:PlaceOrderRequest):
        """
        Used to create an order from provided params and sign it using the private
        key of the account

        Args:
            params (OrderSignatureRequest): parameters to create order with

        Returns:
            OrderSignatureResponse: order raw info and generated signature
        """

        return self.apis.post(
            SERVICE_URLS["ORDERS"]["ORDERS"],
            {
            "symbol": params["symbol"],
            "price": to_bn(params["price"]),
            "quantity": to_bn(params["quantity"]),
            "leverage": to_bn(params["leverage"]),
            "userAddress": self.account.address.lower(),
            "orderType": params["orderType"].value,
            "side": params["side"].value,            
            "reduceOnly": params["reduceOnly"],
            "salt": params["salt"],
            "expiration": params["expiration"],
            "orderSignature": params["orderSignature"],
            "timeInForce": default_enum_value(params, "timeInForce", TIME_IN_FORCE.GOOD_TILL_TIME),
            "postOnly": default_value(params, "postOnly", False),
            "clientId": "firefly-client: {}".format(params["clientId"]) if "clientId" in params else "firefly-client"
            },
            auth_required=True
            )

    ## GETTERS
    def get_order_signer(self,symbol:MARKET_SYMBOLS=None):
        if symbol:
            if symbol.value in self.order_signers.keys():
                return self.order_signers[symbol.value]
            else:
                return "signer doesnt exist"
        else:
            return self.order_signers

    ## Market endpoints
    def get_orderbook(self, params:GetOrderbookRequest):
        return self.apis.get(
            SERVICE_URLS["MARKET"]["ORDER_BOOK"], 
            params
            )

    def get_exchange_status(self):
        return self.apis.get(
            SERVICE_URLS["STATUS"],
            {} 
            )

    def get_market_symbols(self):
        return self.apis.get(
            SERVICE_URLS["MARKET"]["SYMBOLS"],
            {} 
            )

    def get_funding_rate(self,symbol:MARKET_SYMBOLS):
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["FUNDING_RATE"],
            query
        ) 

    def get_market_meta_info(self,symbol:MARKET_SYMBOLS=None):
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["META"], 
            query
            )

    def get_market_data(self,symbol:MARKET_SYMBOLS=None):
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["MARKET_DATA"], 
            query
            )
    
    def get_exchange_info(self,symbol:MARKET_SYMBOLS=None):
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["EXCHANGE_INFO"], 
            query
            )

    def get_market_candle_stick_data(self,params:GetCandleStickRequest):
        params = extract_enums(["symbol","interval"])
        return self.apis.get(
            SERVICE_URLS["MARKET"]["CANDLE_STICK_DATA"], 
            params
            )
    
    def get_market_recent_trades(self,params:GetMarketRecentTradesRequest):
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["MARKET"]["RECENT_TRADE"], 
            params
            ) 

    def get_contract_addresses(self, symbol:MARKET_SYMBOLS=None):
        query = {}
        if symbol:
            query["symbol"] = symbol.value

        return self.apis.get(
            SERVICE_URLS["MARKET"]["CONTRACT_ADDRESSES"], 
            query
            )   

    ## User endpoints
    
    def get_eth_account(self):
        return self.account

    def get_public_address(self):
        return self.account.address

    def get_orders(self,params:GetOrderRequest):
        params = extract_enums(params,["symbol","status"])
        return self.apis.get(
            SERVICE_URLS["USER"]["ORDERS"],
            params,
            True
        )
        
    def get_transaction_history(self,params:GetTransactionHistoryRequest):
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_TRANSACTION_HISTORY"],
            params,
            True
        )
    
    def get_user_position(self,params:GetPositionRequest):
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_POSITIONS"],
            params,
            True
        )

    def get_user_trades(self,params:GetUserTradesRequest):
        params = extract_enums(params,["symbol","type"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_TRADES"],
            params,
            True
        )

    def get_user_account_data(self):
        return self.apis.get(
            service_url = SERVICE_URLS["USER"]["ACCOUNT"],
            query = '',
            auth_required = True
        )
        

    def get_user_default_leverage(self, symbol:MARKET_SYMBOLS):
        account_data_by_market = self.get_user_account_data()["accountDataByMarket"]
        for i in account_data_by_market:
            if symbol.value==i["symbol"]:
                return bn_to_number(i["selectedLeverage"])    
        return "Provided Market Symbol({}) does not exist".format(symbol)
    
