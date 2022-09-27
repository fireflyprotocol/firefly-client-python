
from api_service import APIService
from order_signer import OrderSigner
from onboarding_signer import OnboardingSigner
from utils import *
from enums import ORDER_SIDE, ORDER_TYPE
from constants import ADDRESSES, TIME, SERVICE_URLS
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

        if user_onboarding:
            self.onboard_user()
    
    def get_contract_addresses(self, symbol:MARKET_SYMBOLS=None):
        query = {}
        if symbol:
            query["symbol"] = symbol.value

        return self.apis.get(
            SERVICE_URLS["MARKET"]["CONTRACT_ADDRESSES"], 
            query
            )   

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
            leverage =  to_bn(default_value(params, "leverage", 1)),
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
            leverage=default_value(params, "leverage", 1),
            reduceOnly=default_value(params, "reduceOnly", False),
            salt=order["salt"],
            expiration=order["expiration"],
            orderSignature=order_signature,
            orderType=params["orderType"],
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
            }
            )


    def get_orderbook(self, params:GetOrderbookRequest):
        return self.apis.get(
            SERVICE_URLS["MARKET"]["ORDER_BOOK"], 
            params
            )
