import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_exchange_client import FireflyClient
from constants import Networks
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
    
    # returns user account (having pvt key and pub address)
    user_account = client.get_account()
    print('account:', user_account)

    # returns user public address
    pub_address = client.get_public_address()
    print('pub_address:', pub_address)

    # used to fetch user orders. Pass in statuses of orders to get
    orders = client.get_orders({
        "symbol": MARKET_SYMBOLS.ETH, 
        "statuses": [ORDER_STATUS.OPEN, ORDER_STATUS.PENDING]
        })

    print("User open and pending orders:")
    pprint(orders)

    # fetches user transaction history. Pass page number and size as the route is paginated
    tx_history = client.get_transaction_history({
        "symbol": MARKET_SYMBOLS.ETH,
    })
    print("User transaction history:")    
    pprint(tx_history)

    # gets user current position
    # must add market to client before using this method
    client.add_market(MARKET_SYMBOLS.ETH)
    position = client.get_user_position({"symbol":MARKET_SYMBOLS.ETH})

    print("User position:")    
    pprint(position)

    # fetches user trades
    trades = client.get_user_trades({"symbol":MARKET_SYMBOLS.BTC})
    print("User trades:")    
    pprint(trades)


    # fetches user account's general data like leverage, pnl etc.
    account_data = client.get_user_account_data()
    print("Account data:")    
    pprint(account_data)


    user_leverage = client.get_user_leverage()
    print("Account leverage:", user_leverage)    

    return

if __name__ == "__main__":
    main()