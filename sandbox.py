import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "./src/classes")))

from web3 import Web3
from order_signer import OrderSigner
from constants import Networks
from utils import to_bn
from interfaces import Order

def main():
    ordersAddress = "0x1578dD5561A67081b2136f19f61F2c72D1ca8756"
    private_key = "4d6c9531e0042cc8f7cf13d8c3cf77bfe239a8fed95e198d498ee1ec0b1a7e83"
    signer = OrderSigner(
        Networks["DEV"]["chainId"], 
        ordersAddress, 
        private_key
        )

    order = Order (
        isBuy =  True,
        reduceOnly = False,
        price = to_bn(2),
        quantity = to_bn(1),
        leverage = to_bn(1),
        expiration = 1666541253,
        triggerPrice = 0,
        salt = 123456780,
        maker = "0xFEa83f912CF21d884CDfb66640CfAB6029D940aF",
        taker = ordersAddress
    )    

    order_hash = signer.get_order_hash(order)
    print('Order Hash:', order_hash)


    signature = signer.sign_order(order)
    print('Signature:', signature)

    
if __name__ == "__main__":
    main()