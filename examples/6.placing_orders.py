import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from interfaces import OrderSignatureRequest


def place_limit_order():
    # initialise client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )
    
    # add market that you wish to trade on ETH/BTC are supported currently
    print('Market added:', client.add_market(MARKET_SYMBOLS.ETH))

    # default leverage of account is set to 3 on firefly
    user_leverage = client.get_user_leverage(MARKET_SYMBOLS.ETH)

    # creates a LIMIT order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH,  # market symbol
        price=1300,  # price at which you want to place order
        quantity=0.01, # quantity
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.LIMIT,
        leverage=user_leverage
    )  

    # create signed order
    signed_order = client.create_signed_order(signature_request);

    print("Placing a limit order")
    # place signed order on orderbook
    resp = client.post_signed_order(signed_order)

    # returned order with PENDING state
    print(resp)

    return

def place_market_order():
     # initialise client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )
    
    # add market that you wish to trade on ETH/BTC are supported currently
    print('Market added:', client.add_market(MARKET_SYMBOLS.BTC))

    # default leverage of account is set to 3 on firefly
    user_leverage = client.get_user_leverage(MARKET_SYMBOLS.BTC)

    # creates a LIMIT order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.BTC,  # market symbol
        price=0,  # price at which you want to place order
        quantity=0.01, # quantity
        side=ORDER_SIDE.BUY, 
        orderType=ORDER_TYPE.MARKET,
        leverage=user_leverage
    )  

    # create signed order
    signed_order = client.create_signed_order(signature_request);

    print("Placing a market order")
    # place signed order on orderbook
    resp = client.post_signed_order(signed_order)

    # returned order with PENDING state
    print(resp)


    return

def main():
    place_limit_order()
    place_market_order()
    

if __name__ == "__main__":
    main()