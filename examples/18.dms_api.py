import json
from config import TEST_ACCT_KEY, TEST_SUB_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, Networks, OrderSignatureRequest
import asyncio



async def main():

  client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
  await client.init(True)

  print("User: ", client.get_public_address())
  client.add_market(MARKET_SYMBOLS.ETH)

  countDowns = []
  countDowns.append({
            'symbol': MARKET_SYMBOLS.ETH.value,
            'countDown': 3 * 1000
          }
         )

  
  
  try:
     # sending post request to reset user's count down timer with MARKET_SYMBOL for auto cancellation of order
    postResponse = await client.reset_cancel_on_disconnect_timer({
        "countDowns": countDowns
        })
    print(postResponse)   
    # get request to get user's count down timer for MARKET_SYMBOL
    getResponse = await client.get_cancel_on_disconnect_timer(MARKET_SYMBOLS.ETH)
    print(getResponse)
 
  except Exception as e:
    print(e)
 


  # await clientChild.apis.close_session();
  await client.apis.close_session()


if __name__ == "__main__":
     event_loop = asyncio.get_event_loop()
     event_loop.run_until_complete(main())
