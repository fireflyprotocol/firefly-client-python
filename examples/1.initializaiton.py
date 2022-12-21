from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from pprint import pprint

def main():

  # initialize client
  client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

  print('Account Address:', client.get_public_address());

  # # gets user account data on-chain
  data = client.get_user_account_data()

  pprint(data)


if __name__ == "__main__":
    main()