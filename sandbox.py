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

from sockets import Sockets

from constants import *
from utils import *
from interfaces import *
from enums import *


def main():
    ordersAddress = "0x1578dD5561A67081b2136f19f61F2c72D1ca8756"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    client = FireflyClient(True,Networks["DEV"],private_key,True)
     
    if client.socket.connection_established:
        a = lambda x: print(x)
        client.socket.listen("default",a)
        print(client.socket.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.DOT))
        time.sleep(60)
    client.socket.disconnect()
    print("done")
    

if __name__ == "__main__":
    main()