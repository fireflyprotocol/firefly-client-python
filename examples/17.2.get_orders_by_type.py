'''
    This example shows how users can get their orders based on type and status information.
    The get_orders_by_type route provides a number of optional params that can be 
    mixed together to fetch the exact data that user needs.
'''
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, ORDER_STATUS, ORDER_TYPE
import asyncio

async def main():

    client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
    await client.init(True)

    print("Get all ETH orders regardless of their order type/status")
    orders = await client.get_orders_by_type({
        "symbol": MARKET_SYMBOLS.ETH,
        })    
    print('Received orders: ', len(orders))

    print("Get all market orders based on status (OPEN and PENDING)")
    orders = await client.get_orders_by_type({
        "symbol": MARKET_SYMBOLS.ETH,
        "marketStatuses": [ORDER_STATUS.OPEN, ORDER_STATUS.PENDING]
        })    
    print('Received orders: ', len(orders))

    print("Get all limit orders based on status (OPEN and PENDING)")
    orders = await client.get_orders_by_type({
        "symbol": MARKET_SYMBOLS.ETH,
        "limitStatuses": [ORDER_STATUS.OPEN, ORDER_STATUS.PENDING]
        })    
    print('Received orders: ', len(orders))

    print("Get an order 180318 using id (possible this order is not available anymore)")
    orders = await client.get_orders_by_type({
        "symbol": MARKET_SYMBOLS.ETH,
        "orderId": 180318
        })
    print('Received orders: ', len(orders))

    print("Get orders using hashes (possible these orders are not available anymore)")
    orders = await client.get_orders_by_type({
        "symbol": MARKET_SYMBOLS.ETH,
        "orderHashes": [
        "0x21eeb24b0af6832989484e61294db70e8cf8ce0e030c6cfbbb23f3b3d85f9374",
        "0xd61fe390f6e6d89a884c73927741ba7d2d024e01f65af61f13363403e805e2c0"]
        })
    print('Received orders: ', len(orders))

    await client.close_connections() 


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()