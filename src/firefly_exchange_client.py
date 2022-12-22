from api_service import APIService
from contracts import Contracts
from order_signer import OrderSigner
from onboarding_signer import OnboardingSigner
from utilities import *
from constants import TIME, SERVICE_URLS
from interfaces import *
from eth_account import Account
from sockets import Sockets
from enumerations import *


class FireflyClient:
    def __init__(self, are_terms_accepted, network, private_key, user_onboarding=True):
        self.are_terms_accepted = are_terms_accepted
        self.network = network
        self.w3 = self._connect_w3(self.network["url"])
        self.account = Account.from_key(private_key)
        self.apis = APIService(self.network["apiGateway"])
        self.socket = Sockets(self.network["socketURL"])
        self.contracts = Contracts()
        self.order_signers = {}
        self.contracts.contract_addresses = self.get_contract_addresses()
        self.onboarding_signer = OnboardingSigner()
        

        if "error" in self.contracts.contract_addresses:
            raise Exception("Error initializing client: {}".format(self.contracts.contract_addresses["error"]))

        # adding auxiliaryContracts to contracts class
        for i,j in self.contracts.get_contract_address(market="auxiliaryContractsAddresses").items():
            self.add_contract(name=i,address=j)
        
        # contracts pertaining to markets
        for k, v in self.contracts.contract_addresses.items():
            if 'PERP' in k:
                self.add_contract(name="Perpetual",address=v["Perpetual"], market=k)
        
        if user_onboarding:
            self.apis.auth_token = self.onboard_user()
            self.socket.set_token(self.apis.auth_token)

 

    def onboard_user(self, token:str=None):
        """
            On boards the user address and returns user authentication token.
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

    def add_contract(self,name,address,market=None):
        """
            Adds contracts to the instance's contracts dictionary. 
            The contract name should match the contract's abi name in ./abi directory or a new abi should be added with the desired name.
            Inputs:
                - name(str): The contract name.
                - address(str): The contract address.
                - market(str): The market (ETH/BTC) this contract belongs to (required for market specific contracts).
        """
        abi = self.contracts.get_contract_abi(name)
        if market:
            contract=self.w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
            self.contracts.set_contracts(market=market,name=name,contract=contract)
        else:
            contract=self.w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
            self.contracts.set_contracts(name=name,contract=contract)
        return 

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
            price = to_big_number(params["price"]),
            quantity =  to_big_number(params["quantity"]),
            leverage =  to_big_number(default_value(params, "leverage", 1)),
            maker =  self.account.address.lower(),
            reduceOnly =  default_value(params, "reduceOnly", False),
            triggerPrice =  0,
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
            leverage=default_value(params, "leverage", 1),
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
            signer:OrderSigner = self._get_order_signer(params["symbol"])
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
        order_signer:OrderSigner = self._get_order_signer(symbol)
        cancel_hash = order_signer.sign_cancellation_hash(order_hash)
        hash_sig = order_signer.sign_hash(cancel_hash,self.account.key.hex(), "01")
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
            "statuses":[ORDER_STATUS.OPEN, ORDER_STATUS.PARTIAL_FILLED]
        })

        hashes = []
        for i in orders:
            hashes.append(i["hash"])
        
        if len(hashes) > 0:
            req = self.create_signed_cancel_orders(symbol,hashes)
            return self.post_cancel_order(req)

        return False
    
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
            "price": to_big_number(params["price"]),
            "quantity": to_big_number(params["quantity"]),
            "leverage": to_big_number(params["leverage"]),
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

    ## Contract calls
    def deposit_margin_to_bank(self, amount):
        """
            Deposits given amount of USDC from user's account to margin bank

            Inputs:
                amount (number): quantity of usdc to be deposited to bank in base decimals (1,2 etc)

            Returns:
                Boolean: true if amount is successfully deposited, false otherwise
        """

        usdc_contract = self.contracts.get_contract(name="USDC");
        mb_contract = self.contracts.get_contract(name="MarginBank");

        amount = to_big_number(amount,6);

        # approve funds on usdc
        
        construct_txn = usdc_contract.functions.approve(
            mb_contract.address, 
            amount).buildTransaction({
                'from': self.account.address,
                'nonce': self.w3.eth.getTransactionCount(self.account.address),
            })

        self._execute_tx(construct_txn)

        # deposit to margin bank
        construct_txn = mb_contract.functions.depositToBank(
            self.account.address, 
            amount).buildTransaction({
                'from': self.account.address,
                'nonce': self.w3.eth.getTransactionCount(self.account.address),
                })

        self._execute_tx(construct_txn)

        return True;

    def withdraw_margin_from_bank(self, amount):
        """
            Withdraws given amount of usdc from margin bank if possible

            Inputs:
                amount (number): quantity of usdc to be withdrawn from bank in base decimals (1,2 etc)

            Returns:
                Boolean: true if amount is successfully withdrawn, false otherwise
        """

        mb_contract = self.contracts.get_contract(name="MarginBank");
        amount = to_big_number(amount,6);

        # withdraw from margin bank
        construct_txn = mb_contract.functions.withdrawFromBank(
            self.account.address, 
            amount).buildTransaction({
                'from': self.account.address,
                'nonce': self.w3.eth.getTransactionCount(self.account.address),
                })

        self._execute_tx(construct_txn)

        return True;

    def adjust_leverage(self, symbol, leverage):
        """
            Adjusts user leverage to the provided one for their current position on-chain and off-chain.
            If a user has no position for the provided symbol, leverage only recorded off-chain

            Inputs:
                symbol (MARKET_SYMBOLS): market for which to adjust user leverage
                leverage (number): new leverage to be set. Must be in base decimals (1,2 etc.)

            Returns:
                Boolean: true if the leverage is successfully adjusted
        """

        user_position = self.get_user_position({"symbol":symbol})

        # implies user has an open position on-chain, perform on-chain leverage update
        if(user_position != {}):
            perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value);
            construct_txn = perp_contract.functions.adjustLeverage(
                self.account.address, 
                to_big_number(leverage)).buildTransaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.getTransactionCount(self.account.address),
                    })

            self._execute_tx(construct_txn)

        else:
            self.apis.post(
                SERVICE_URLS["USER"]["ADJUST_LEVERAGE"],
                {
                    "symbol": symbol.value,
                    "address": self.account.address,
                    "leverage": to_big_number(leverage),
                    "marginType": MARGIN_TYPE.ISOLATED.value,
                    },
                auth_required=True
                )
        
        return True
 
    def adjust_margin(self, symbol, operation, amount):
        """
            Adjusts user's on-chain position by adding or removing the specified amount of margin.
            Performs on-chain contract call, the user must have gas tokens
            Inputs:
                symbol (MARKET_SYMBOLS): market for which to adjust user leverage
                operation (ADJUST_MARGIN): ADD/REMOVE adding or removing margin to position
                amount (number): amount of margin to be adjusted

            Returns:
                Boolean: true if the margin is adjusted
        """

        user_position = self.get_user_position({"symbol":symbol})

        if(user_position == {}):
            raise(Exception("User has no open position on market: {}".format(symbol)))
        else:
            perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value);
            on_chain_call = perp_contract.functions.addMargin if operation == ADJUST_MARGIN.ADD  else perp_contract.functions.removeMargin

            construct_txn = on_chain_call(
                self.account.address, 
                to_big_number(amount)).buildTransaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.getTransactionCount(self.account.address),
                    })

            self._execute_tx(construct_txn)
        
        return True
 
    def get_native_chain_token_balance(self):
        """
            Returns user's native chain token (ETH/BOBA) balance
        """
        try:
            return big_number_to_base(self.w3.eth.get_balance(self.w3.toChecksumAddress(self.account.address)))
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_usdc_balance(self):
        """
            Returns user's USDC token balance on Firefly.
        """
        try:
            contract = self.contracts.get_contract(name="USDC")
            raw_bal = contract.functions.balanceOf(self.account.address).call();
            return big_number_to_base(int(raw_bal), 6)
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_margin_bank_balance(self):
        """
            Returns user's Margin Bank balance.
        """
        try:
            contract = self.contracts.get_contract(name="MarginBank")
            return contract.functions.getAccountBankBalance(self.account.address).call()/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))


    
    ## Market endpoints
    
    def get_orderbook(self, params:GetOrderbookRequest):
        """
            Returns a dictionary containing the orderbook snapshot.
            Inputs:
                - params(GetOrderbookRequest): the order symbol and limit(orderbook depth) 
            Returns:
                - dict: Orderbook snapshot
        """
        params = extract_enums(params, ["symbol"])

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
        return self.apis.get(SERVICE_URLS["MARKET"]["STATUS"], {})

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
            Returns a dictionary containing the current funding rate on market.
            Inputs:
                - symbol(MARKET_SYMBOLS): symbol of market
            Returns:
                - dict: Funding rate into
        """
        return self.apis.get(
            SERVICE_URLS["MARKET"]["FUNDING_RATE"],
            {"symbol": symbol.value}
        ) 

    def get_market_meta_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market meta info.
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: meta info
        """
        query = {"symbol": symbol.value } if symbol else {}

        return self.apis.get(
            SERVICE_URLS["MARKET"]["META"], 
            query
            )

    def get_market_data(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market's current data about best ask/bid, 24 hour volume, market price etc..
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: meta info
        """
        query = {"symbol": symbol.value } if symbol else {}

        return self.apis.get(
            SERVICE_URLS["MARKET"]["MARKET_DATA"], 
            query
            )
    
    def get_exchange_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing exchange info for market(s). The min/max trade size, max allowed oi open
            min/max trade price, step size, tick size etc...
            Inputs:
                - symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                - dict: exchange info
        """
        query = {"symbol": symbol.value } if symbol else {}
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
        params = extract_enums(params, ["symbol","interval"])
        
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
        params = extract_enums(params, ["symbol", "traders"])

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
        query = {"symbol": symbol.value } if symbol else {}

        return self.apis.get(
            SERVICE_URLS["MARKET"]["CONTRACT_ADDRESSES"], 
            query
            )   

    ## User endpoints
    
    def get_account(self):
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
        
    def get_user_leverage(self, symbol:MARKET_SYMBOLS):
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
                return int(big_number_to_base(i["selectedLeverage"]))    

        # default leverage on system is 3
        # todo fetch from exchange info route
        return 3

       
    ## Internal methods
    def _get_order_signer(self,symbol:MARKET_SYMBOLS=None):
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
                raise(Exception("Signer does not exist. Make sure to add market"))
        else:
            return self.order_signers

    def _execute_tx(self, transaction):
        """
            An internal function to create signed tx and wait for its receipt
        Args:
            transaction: A constructed txn using self.account address

        Returns:
            tx_receipt: a receipt of txn mined on-chain
        """
        tx_create = self.w3.eth.account.signTransaction(transaction, self.account.key)
        tx_hash = self.w3.eth.sendRawTransaction(tx_create.rawTransaction)
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def _connect_w3(self,url):
        """
            Creates a connection to Web3 RPC given the RPC url.
        """
        try:
            return Web3(Web3.HTTPProvider(url))
        except:
            raise(Exception("Failed to connect to Host: {}".format(url)))
           