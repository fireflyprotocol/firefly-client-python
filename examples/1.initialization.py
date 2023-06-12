from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks
from pprint import pprint
import asyncio



async def main():
  # initialize client
  client = FireflyClient(
      True, # agree to terms and conditions
      Networks[TEST_NETWORK], # network to connect with
      TEST_ACCT_KEY, # private key of wallet
      )

  # initialize the client
  # on boards user on firefly. Must be set to true for first time use
  await client.init(True,"") 
  
  print('Account Address:', client.get_public_address()) 

  # # gets user account data on-chain
  data = await client.get_user_account_data()

  # close aio http connection
  await client.apis.close_session()

  pprint(data)

if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()