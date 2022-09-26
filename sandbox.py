import os
import sys
# from prettyformatter import pprint
from pprint import pprint
import time

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src/classes")))

from web3 import Web3
from order_signer import OrderSigner
from firefly_client import FireflyClient

from constants import *
from utils import *
from interfaces import *
from enums import *

def post_order_test(client:FireflyClient):
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.DOT, 
        price=2.5, 
        quantity=0.1, 
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.MARKET,
        leverage= 2,
        expiration=1,
        reduceOnly=False,
        salt=10
    )  
    print(signature_request)
    signed_order = client.create_signed_order(signature_request);
    # pprint(signed_order)

    # order_request = PlaceOrderRequest(
    #     signed_order, 
    #     postOnly=True)

    # resp = client.post_signed_order(order_request)
    
def test_getters_with_symbol(client):
    resp = client.get_market_meta_info(MARKET_SYMBOLS.DOT)
    print(resp)
    resp = client.get_exchange_info(MARKET_SYMBOLS.DOT)
    print(resp)
    resp = client.get_market_data(MARKET_SYMBOLS.DOT)
    print(resp)
    req = GetMarketRecentTradesRequest(symbol=MARKET_SYMBOLS.DOT,pageSize=10)
    resp = client.get_market_recent_trades(params=req)
    print(resp)
    req = GetCandleStickRequest(symbol=MARKET_SYMBOLS.DOT, interval=Interval._1m)
    resp = client.get_market_candle_stick_data(req)
    print(resp)


def main():
    ordersAddress = "0x1578dD5561A67081b2136f19f61F2c72D1ca8756"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    client = FireflyClient(
        True,
        Networks["DEV"], 
        private_key
        )
    client.add_market(MARKET_SYMBOLS.DOT, ordersAddress)
    test_getters_with_symbol(client)
    

    
if __name__ == "__main__":
    main()