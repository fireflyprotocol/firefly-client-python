from api_service import APIService
from contracts import Contracts
from order_signer import OrderSigner
from onboarding_signer import OnboardingSigner
from utils import *
from enums import ORDER_SIDE, ORDER_TYPE
from constants import ADDRESSES, TIME, SERVICE_URLS
from interfaces import *
from enums import MARKET_SYMBOLS
from eth_account import Account
from sockets import Sockets


class FireflyClient:
    def __init__(self, are_terms_accepted, network, private_key, user_onboarding=True):
        self.are_terms_accepted = are_terms_accepted
        self.network = network
        self.account = Account.from_key(private_key)
        self.apis = APIService(self.network["apiGateway"])
        self.socket = Sockets(self.network["socketURL"])
        self.contracts = Contracts(self.network["url"])
        self.contracts.set_account(private_key) # assigning account to contracts instance 
        self.order_signers = {}
        self.contracts.contract_addresses = self.get_contract_addresses()
        self.onboarding_signer = OnboardingSigner()
        
        # todo fetch from api
        self.default_leverage = 3

        # adding auxiliaryContracts to contracts class
        for i,j in self.contracts.contract_addresses["auxiliaryContractsAddresses"].items():
            self.contracts.add_contract(name=i,address=j)
        
        if user_onboarding:
            self.apis.auth_token = self.onboard_user()

    def onboard_user(self, token:str=None):
        """
            Onboards the user addresss and returns user autherntication token.
            Inputs:
                - token: user access token, if you possess one.
            Returns:
                - str: user authorization token
        """
        user_auth_token = token
        
        # if no auth token provided create on
        if not user_auth_token:
            onboarding_signature = self.onboarding_signer.create_signature(
                self.network["onboardingUrl"], 
                self.account.key)

            response = self.authorize_signed_hash(onboarding_signature);
            
            if 'error' in response:
                raise SystemError("Authorization error: {}".format(response['error']['message']))

            user_auth_token = response['token']

        return user_auth_token

    def authorize_signed_hash(self, signed_hash:str):
        """
            Registers user as an authorized user on server and returns authorization token.
            Inputs:
                - signed_hash: signed onboarding hash
            Returns:
                - dict: response from user authorization API Firefly
        """
        return self.apis.post(
            SERVICE_URLS["USER"]["AUTHORIZE"],
            {
                "signature": signed_hash,
                "userAddress": self.account.address,
                "isTermAccepted": self.are_terms_accepted,
            })

    def add_market(self, symbol: MARKET_SYMBOLS, trader_contract=None):
        """
            Adds Order signer for market to instance's order_signers dict.
            Inputs:
                - symbol(MARKET_SYMBOLS): Market symbol of order signer.
                - orders_contract(str): Contract address of the orders contract.
            
            Returns:
                - bool: indicating whether the market was successfully added
        """
        symbol_str = symbol.value
        # if signer for market already exists return false
        if (symbol_str in self.order_signers):
            return False 
          
        # if orders contract address is not provided get 
        # from addresses retrieved from dapi
        if trader_contract == None:
            try:
                trader_contract = self.contracts.contract_addresses[symbol_str]["IsolatedTrader"]
            except:
                raise SystemError("Can't find orders contract address for market: {}".format(symbol_str))

        self.order_signers[symbol_str] = OrderSigner(
            self.network["chainId"],
            trader_contract
            )
        return True 

    def create_order_to_sign(self, params:OrderSignatureRequest):
        """
            Creates order signature request for an order.
            Inputs:
                - params (OrderSignatureRequest): parameters to create order with 
            
            Returns:
                - Order: order raw info
        """
        expiration = current_unix_timestamp()        
        # MARKET ORDER - set expiration of 1 minute
        if (params["orderType"] == ORDER_TYPE.MARKET):
            expiration += TIME["SECONDS_IN_A_MINUTE"]
        # LIMIT ORDER - set expiration of 30 days
        else:
            expiration += TIME["SECONDS_IN_A_MONTH"] 

        return Order (
            isBuy = params["side"] == ORDER_SIDE.BUY,
            price = to_bn(params["price"]),
            quantity =  to_bn(params["quantity"]),
            leverage =  to_bn(default_value(params, "leverage", self.default_leverage)),
            maker =  self.account.address.lower(),
            reduceOnly =  default_value(params, "reduceOnly", False),
            triggerPrice =  to_bn(0),
            expiration =  default_value(params, "expiration", expiration),
            salt =  default_value(params, "salt", random_number(1000000)),
            )

    def create_signed_order(self, params:OrderSignatureRequest):
        """
            Create an order from provided params and signs it using the private 
            key of the account
        Inputs:
            - params (OrderSignatureRequest): parameters to create order with
 
        Returns:
            - OrderSignatureResponse: order raw info and generated signature
        """
        
        # from params create order to sign
        order = self.create_order_to_sign(params)

        symbol = params["symbol"].value
        order_signer = self.order_signers.get(symbol) 

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
        """
            Creates a cancel order request from provided params and signs it using the private
            key of the account

        Inputs:
            - params (OrderSignatureRequest): parameters to create cancel order with
 
        Returns:
            - OrderSignatureResponse: generated cancel signature 
        """
        try:
            signer:OrderSigner = self.get_order_signer(params["symbol"])
            order_to_sign = self.create_order_to_sign(params)
            hash = signer.get_order_hash(order_to_sign)
            return self.create_signed_cancel_orders(params["symbol"],hash)
        except Exception as e:
            return ""

    def create_signed_cancel_orders(self,symbol:MARKET_SYMBOLS,order_hash:list):
        """
            Creates a cancel order from provided params and sign it using the private
            key of the account

        Inputs:
            params (list): a list of order hashes
 
        Returns:
            OrderCancellationRequest: containing symbol, hashes and signature
        """
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
        """
            POST cancel order request to Firefly
            Inputs:
                - params(dict): a dictionary with OrderCancellationRequest required params
            Returns:
                - dict: response from orders delete API Firefly
        """
        return self.apis.delete(
            SERVICE_URLS["ORDERS"]["ORDERS_HASH"],
            {
            "symbol": params["symbol"],
            "orderHashes":params["hashes"],
            "cancelSignature":params["signature"]
            },
            auth_required=True
            )
    
    def cancel_all_open_orders(self,symbol:MARKET_SYMBOLS):
        """
            GETs all open orders for the specified symbol, creates a cancellation request 
            for all orders and POSTs the cancel order request to Firefly
            Inputs:
                - symbol(MARKET_SYMBOLS) 
            Returns:
                - dict: response from orders delete API Firefly
        """
        orders = self.get_orders({
            "symbol":symbol,
            "status":ORDER_STATUS.OPEN
        })
        hashes = []
        for i in orders:
            hashes.append(i["hash"])
        req = self.create_signed_cancel_orders(symbol,hashes)
        return self.post_cancel_order(req)
    
    def post_signed_order(self, params:PlaceOrderRequest):
        """
            Creates an order from provided params and signs it using the private
            key of the account

            Inputs:
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
        """
            Returns the order signer for the specified symbol, else returns a dictionary of symbol -> order signer
            Inputs:
                - symbol(MARKET_SYMBOLS): the symbol to get order signer for, optional
            Returns:
                - dict/order signer object
        """
        if symbol:
            if symbol.value in self.order_signers.keys():
                return self.order_signers[symbol.value]
            else:
                return "signer doesnt exist"
        else:
            return self.order_signers

    ## Market endpoints
    def get_orderbook(self, params:GetOrderbookRequest):
        """
            Returns a dictionary containing the orderbook snapshot.
            Inputs:
                - params(GetOrderbookRequest): the order symbol and limit(orderbook depth) 
            Returns:
                - dict: Orderbook snapshot
        """
        return self.apis.get(
            SERVICE_URLS["MARKET"]["ORDER_BOOK"], 
            params
            )

    def get_exchange_status(self):
        """
            Returns a dictionary containing the exchange status.
            Returns:
                - dict: exchange status
        """
        return self.apis.get(
            SERVICE_URLS["STATUS"],
            {} 
            )

    def get_market_symbols(self):
        """
            Returns a list of active market symbols.
            Returns:
                - list: active market symbols
        """
        return self.apis.get(
            SERVICE_URLS["MARKET"]["SYMBOLS"],
            {} 
            )

    def get_funding_rate(self,symbol:MARKET_SYMBOLS):
        """
            Returns a dictionary containing the orderbook snapshot.
            Inputs:
                - params(GetOrderbookRequest): the order symbol and limit(orderbook depth) 
            Returns:
                - dict: Orderbook snapshot
        """
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["FUNDING_RATE"],
            query
        ) 

    def get_market_meta_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market meta info.
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: meta info
        """
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["META"], 
            query
            )

    def get_market_data(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market meta info.
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: meta info
        """
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["MARKET_DATA"], 
            query
            )
    
    def get_exchange_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing exchange.
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: exchange info
        """
        query = {}
        if symbol:
            query["symbol"] = symbol.value
        return self.apis.get(
            SERVICE_URLS["MARKET"]["EXCHANGE_INFO"], 
            query
            )

    def get_market_candle_stick_data(self,params:GetCandleStickRequest):
        """
            Returns a list containing the candle stick data.
            Inputs:
                - params(GetCandleStickRequest): params required to fetch candle stick data  
            Returns:
                - list: the candle stick data
        """
        params = extract_enums(["symbol","interval"])
        return self.apis.get(
            SERVICE_URLS["MARKET"]["CANDLE_STICK_DATA"], 
            params
            )
    
    def get_market_recent_trades(self,params:GetMarketRecentTradesRequest):
        """
            Returns a list containing the recent trades data.
            Inputs:
                - params(GetCandleStickRequest): params required to fetch candle stick data  
            Returns:
                - ist: the recent trades 
        """
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["MARKET"]["RECENT_TRADE"], 
            params
            ) 

    def get_contract_addresses(self, symbol:MARKET_SYMBOLS=None):
        """
            Returns all contract addresses for the provided market.
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol
            Returns:
                - dict: all the contract addresses
        """
        query = {}
        if symbol:
            query["symbol"] = symbol.value

        return self.apis.get(
            SERVICE_URLS["MARKET"]["CONTRACT_ADDRESSES"], 
            query
            )   

    ## User endpoints
    
    def get_eth_account(self):
        """
            Returns the user account object 
        """
        return self.account

    def get_public_address(self):
        """
            Returns the user account public address
        """
        return self.account.address

    def get_orders(self,params:GetOrderRequest):
        """
            Returns a list of orders.
            Inputs:
                - params(GetOrderRequest): params required to query orders (e.g. symbol,statuses) 
            Returns:
                - list: a list of orders 
        """
        params = extract_enums(params,["symbol","statuses"])
        return self.apis.get(
            SERVICE_URLS["USER"]["ORDERS"],
            params,
            True
        )
        
    def get_transaction_history(self,params:GetTransactionHistoryRequest):
        """
            Returns a list of transaction.
            Inputs:
                - params(GetTransactionHistoryRequest): params to query transactions (e.g. symbol) 
            Returns:
                - list: a list of transactions
        """
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_TRANSACTION_HISTORY"],
            params,
            True
        )
    
    def get_user_position(self,params:GetPositionRequest):
        """
            Returns a list of positions.
            Inputs:
                - params(GetPositionRequest): params required to query positions (e.g. symbol) 
            Returns:
                - list: a list of positions
        """
        params = extract_enums(params,["symbol"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_POSITIONS"],
            params,
            True
        )

    def get_user_trades(self,params:GetUserTradesRequest):
        """
            Returns a list of user trades.
            Inputs:
                - params(GetUserTradesRequest): params to query trades (e.g. symbol) 
            Returns:
                - list: a list of positions
        """
        params = extract_enums(params,["symbol","type"])
        return self.apis.get(
            SERVICE_URLS["USER"]["USER_TRADES"],
            params,
            True
        )

    def get_user_account_data(self):
        """
            Returns user account data.
        """
        return self.apis.get(
            service_url = SERVICE_URLS["USER"]["ACCOUNT"],
            query = '',
            auth_required = True
        )
        
    def get_user_default_leverage(self, symbol:MARKET_SYMBOLS):
        """
            Returns user market default leverage.
            Inputs:
                - symbol(MARKET_SYMBOLS): market symbol to get user market default leverage for. 
            Returns:
                - str: user default leverage 
        """
        account_data_by_market = self.get_user_account_data()["accountDataByMarket"]
        for i in account_data_by_market:
            if symbol.value==i["symbol"]:
                return bn_to_number(i["selectedLeverage"])    
        return "Provided Market Symbol({}) does not exist".format(symbol)
    
    def get_usdc_balance(self):
        """
            Returns user USDC balance.
        """
        return self.contracts.get_usdc_balance()
    
    def get_margin_bank_balance(self):
        """
            Returns user Margin bank balance.
        """
        return self.contracts.get_margin_bank_balance()


    