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
from firefly_sockets import Sockets

from constants import *
from utils import *
from interfaces import *
from enums import *

import socketio

# standard Python
sio = socketio.Client()

class test_socket:
    def __init__(self,url) -> None:
        sio.connect(url)


    @sio.event
    def connect():
        
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    @sio.on('*')
    def catch_all(event, data):
        pass



def main():
    ordersAddress = "0x1578dD5561A67081b2136f19f61F2c72D1ca8756"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    x = Sockets(Networks["DEV"]["socketURL"])
    time.sleep(20)
    print(x.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.DOT))
    while True:
        pass
    

if __name__ == "__main__":
    main()