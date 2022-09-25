import os
import sys
# from prettyformatter import pprint
from pprint import pprint

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
    ordersAddress = "0x1578dD5561A67081b2136f19f61F2c72D1ca8756"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    # signer = OrderSigner(
    #     Networks["DEV"]["chainId"], 
    #     ordersAddress, 
    #     )

    # order = Order (
    #     isBuy =  True,
    #     reduceOnly = False,
    #     price = to_bn(2),
    #     quantity = to_bn(1),
    #     leverage = to_bn(1),
    #     expiration = 1666541253,
    #     triggerPrice = 0,
    #     salt = 123456780,
    #     maker = "0xFEa83f912CF21d884CDfb66640CfAB6029D940aF",
    #     taker = ordersAddress
    # )    

    # # order_hash = signer.get_order_hash(order)
    # # print('Order Hash:', order_hash)


    # # signature = signer.sign_order(order, private_key)
    # # print('Signature:', signature)

    client = FireflyClient(
        True,
        Networks["DEV"], 
        private_key
        )

    client.add_market(MARKET_SYMBOLS.DOT, ordersAddress)

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

    signed_order = client.create_signed_order(signature_request);
    # pprint(signed_order)

    order_request = PlaceOrderRequest(
        signed_order, 
        postOnly=True)

    resp = client.post_signed_order(order_request)
    
    # response = client.get_orderbook({
    #     "symbol":MARKET_SYMBOLS.DOT.value
    # })

    print(resp)

if __name__ == "__main__":
    main()