import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ADJUST_MARGIN
from utilities import big_number_to_base
from pprint import pprint


def main():

    # initialise client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )
    
    position = client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))

    # adding 100$ from our margin bank into our BTC position on-chain
    # must have native chain tokens to pay for gas fee
    client.adjust_margin(MARKET_SYMBOLS.BTC, ADJUST_MARGIN.ADD, 100);

    # get updated position margin. Note it can take a few seconds to show updates
    # to on-chain positions on exchange as off-chain infrastructure waits for blockchain
    # to emit position update event
    position = client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))


    # removing 100$ from margin
    client.adjust_margin(MARKET_SYMBOLS.BTC, ADJUST_MARGIN.REMOVE, 100);

    position = client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))


    # will throw as user does not have any open position on ETH to adjust margin on
    client.adjust_margin(MARKET_SYMBOLS.ETH, ADJUST_MARGIN.ADD, 100);



if __name__ == "__main__":
    main()