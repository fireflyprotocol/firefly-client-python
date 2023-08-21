'''
    This example shows how users can get their open orders information.
    The get_open_orders route provides a number of optional params that can be 
    mixed together to fetch the exact data that user needs.
'''
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS
import asyncio

async def main():

    client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
    await client.init(True)


    print("Get all ETH market open orders")
    orders = await client.get_open_orders({
        "symbol": MARKET_SYMBOLS.ETH,
        })    
    print('Received orders: ', len(orders))

    print("Get all ETH market open orders as sub-account)
    orders = await client.get_open_orders({
        "symbol": MARKET_SYMBOLS.ETH,
        "parentAddress": "0x89658857625254032315C3559e449877594D5f1f"
        })
    print('Received orders: ', len(orders))

    await client.close_connections() 


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()