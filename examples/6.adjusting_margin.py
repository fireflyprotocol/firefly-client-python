from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ADJUST_MARGIN
from utilities import big_number_to_base
import asyncio

async def main():

    # initialize client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )
    
    position = await client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))

    # adding 100$ from our margin bank into our BTC position on-chain
    # must have native chain tokens to pay for gas fee
    await client.adjust_margin(MARKET_SYMBOLS.BTC, ADJUST_MARGIN.ADD, 100);

    # get updated position margin. Note it can take a few seconds to show updates
    # to on-chain positions on exchange as off-chain infrastructure waits for blockchain
    # to emit position update event
    position = await client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))


    # removing 100$ from margin
    await client.adjust_margin(MARKET_SYMBOLS.BTC, ADJUST_MARGIN.REMOVE, 100);

    position = await client.get_user_position({"symbol":MARKET_SYMBOLS.BTC});
    print("Current margin in position:", big_number_to_base(position["margin"]))


    # will throw as user does not have any open position on ETH to adjust margin on
    await client.adjust_margin(MARKET_SYMBOLS.ETH, ADJUST_MARGIN.ADD, 100);



if __name__ == "__main__":
    asyncio.run(main())