import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_client import FireflyClient
from constants import Networks
from interfaces import OrderCancellationRequest
from enumerations import MARKET_SYMBOLS, ORDER_STATUS
from pprint import pprint


def main():

    # initialise client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

    # must add market before cancelling its orders
    client.add_market(MARKET_SYMBOLS.ETH)

    # get user open orders
    open_orders = client.get_orders({
        "symbol": MARKET_SYMBOLS.ETH, 
        "statuses": [ORDER_STATUS.OPEN]
        })

    
    # sign order for cancellation using hash
    cancellation_request = client.create_signed_cancel_orders(MARKET_SYMBOLS.ETH, order_hash=[open_orders[0]['hash']])

    resp = client.post_cancel_order(cancellation_request)
    
    print(resp)

if __name__ == "__main__":
    main()