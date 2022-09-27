import os
import sys
from pprint import pprint

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src/classes")))

from web3 import Web3
from order_signer import OrderSigner
from firefly_client import FireflyClient
from onboarding_signer import OnboardingSigner

from constants import *
from utils import *
from interfaces import *
from enums import *

def main():
    ordersAddress = "0x8C6eDe33D167D416b32eDd568C3578B0deF9bB8D"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    
    client = FireflyClient(
        True,
        Networks["TESTNET"], 
        private_key,
        False
        )

    client.add_market(MARKET_SYMBOLS.BTC, ordersAddress)

    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.BTC, 
        price=2.5, 
        quantity=0.1, 
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.MARKET,
        leverage= 2,
        expiration=1,
        reduceOnly=False,
        salt=10
    )  

    signed_order = client.create_signed_order(signature_request);
    pprint(signed_order)

    # does not work right now because dapi is not able to resolve signature
    # client.onboard_user()
    
if __name__ == "__main__":
    main()