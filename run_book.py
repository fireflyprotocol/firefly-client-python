from asyncio import constants
import os
import sys
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


def main():
    private_key = "6f2ad7a2fde3ee1da954a5910a0a33c4115b24edf052d0612264e45bdaf12437"
    
    # initialize client
    client = FireflyClient(
        True,
        Networks["DEV"], 
        private_key,
        )

    # add eth/btc market
    client.add_market(MARKET_SYMBOLS.BTC)

    # create order to sign
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.BTC, 
        price=500, 
        quantity=0.01, 
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.LIMIT,
        reduceOnly=False,
        leverage=3,
    )  

    # sign created order
    signed_order = client.create_signed_order(signature_request);

    # post signed order to exchange
    resp = client.post_signed_order(signed_order)

    print(resp)
    
    return

if __name__ == "__main__":
    main()
