# Firefly Client Library - Python
Python client library to interact with firefly api gateway to place orders on firefly exchange and to interact with on-chain firefly contracts.

### How to use

```
from firefly_exchange_client import FireflyClient
from constants import Networks
from pprint import pprint

def main():

  # initialize client
  client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        "0x.....", # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

  print('Account Address:', client.get_public_address());

  # # gets user account data on-chain
  data = client.get_user_account_data()

  pprint(data)

```

Look at [example](https://github.com/fireflyprotocol/firefly_exchange_client/tree/main/examples) directory to learn more about client usage.