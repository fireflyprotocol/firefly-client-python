from config import TEST_ACCT_KEY, TEST_SUB_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, MARKET_SYMBOLS, Networks
import asyncio


async def main():

  client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
  await client.init(True)

  print("client: ", client.get_public_address())


  # # closes position when market is delisted
  status = await client.close_position(MARKET_SYMBOLS.ETH)
  print("Close position : {}".format(status))

  await client.close_connections()


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()