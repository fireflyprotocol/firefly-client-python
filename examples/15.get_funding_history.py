from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS
from pprint import pprint
import asyncio

from interfaces import GetFundingHistoryRequest

# initialize client
client = FireflyClient(
    True, # agree to terms and conditions
    Networks[TEST_NETWORK], # network to connect with
    TEST_ACCT_KEY, # private key of wallet
    True, # on boards user on firefly. Must be set to true for first time use
)

async def main():

    # create a funding history request
    funding_history_request = GetFundingHistoryRequest(
        symbol=MARKET_SYMBOLS.ETH,  # market symbol
        pageSize=50, # gets provided number of payments <= 50
        cursor=0 # fetch a particular page. A single page contains upto 50 records
    )

    # submit request for funding history
    funding_history_response = await client.get_funding_history(funding_history_request)

    # returns funding history response
    pprint(funding_history_response)


if __name__ == "__main__":
    asyncio.run(main())