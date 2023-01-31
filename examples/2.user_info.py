from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS
from pprint import pprint
import asyncio

# initialize client
client = FireflyClient(
    True, # agree to terms and conditions
    Networks[TEST_NETWORK], # network to connect with
    TEST_ACCT_KEY, # private key of wallet
    True, # on boards user on firefly. Must be set to true for first time use
    )

async def main():

    # gets user account data on firefly exchange
    data = await client.get_user_account_data()

    pprint(data)

    position = await client.get_user_position({"symbol":MARKET_SYMBOLS.ETH})
    
    # returns {} when user has no position
    pprint(position)

    position = await client.get_user_position({"symbol":MARKET_SYMBOLS.BTC})
    
    # returns user position if exists
    pprint(position)


if __name__ == "__main__":
    asyncio.run(main())