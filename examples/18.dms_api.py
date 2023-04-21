import json
from config import TEST_ACCT_KEY, TEST_SUB_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, Networks, OrderSignatureRequest
import asyncio



async def main():

  clientParent = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
  await clientParent.init(True)

  print("Parent: ", clientParent.get_public_address())
  clientParent.add_market(MARKET_SYMBOLS.ETH)

  response = await clientParent.get_cancel_on_disconnect_timer(MARKET_SYMBOLS.ETH)
  countDowns = []
  countDowns.append({
            'symbol': MARKET_SYMBOLS.ETH.value,
            'countDown': 60 * 1000
          }
         )


  response = await clientParent.reset_cancel_on_disconnect_timer({
        "countDowns": countDowns,
        "address":""
        })

  print(response)

  # await clientChild.apis.close_session();
  await clientParent.apis.close_session()


if __name__ == "__main__":
     event_loop = asyncio.get_event_loop()
     event_loop.run_until_complete(main())
