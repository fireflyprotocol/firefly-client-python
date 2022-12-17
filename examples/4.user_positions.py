import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS



def main():

    # initialise client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

    position = client.get_user_position({"symbol":MARKET_SYMBOLS.ETH})
    
    # returns {} when user has no position
    print("No Position:", position)

    position = client.get_user_position({"symbol":MARKET_SYMBOLS.BTC})
    # returns user position if exists
    print("Position:", position)


if __name__ == "__main__":
    main()