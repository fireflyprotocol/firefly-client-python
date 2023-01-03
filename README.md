# Firefly Client Library
[<img alt="Firefly logo" src="https://raw.githubusercontent.com/fireflyprotocol/firefly_exchange_client/main/res/banner.png" />](#)

<div align="center">

![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/fireflyprotocol/firefly_exchange_client/publish_to_pypi.yml)
[![pypi version](https://img.shields.io/pypi/v/firefly_exchange_client?logo=pypi)](https://pypi.org/project/firefly_exchange_client/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
</div>



Python Client for the Firefly Exchange API and Smart Contracts.
​
### How to use
The package can be installed from [PyPi](https://pypi.org/project/firefly-exchange-client/) using pip:
```
pip install firefly-exchange-client
```

Find complete documentation on the library at https://docs.firefly.exchange/.

**Getting Started**
When initializing the client, users must accept [terms and conditions](https://firefly.exchange/terms-of-use) and define network object containing the following values:
```
{
    "url": "https://goerli-rollup.arbitrum.io/rpc",
    "chainId": 421613,
    "apiGateway": "https://dapi-testnet.firefly.exchange",
    "socketURL": "wss://dapi-testnet.firefly.exchange",
    "webSocketURL": "",
    "onboardingUrl": "https://testnet.firefly.exchange",
},
```
Users can import predefined networks from [constants](https://github.com/fireflyprotocol/firefly_exchange_client/blob/main/src/constants.py):
```
from constants import Networks
```
For testing purposes use `Networks[TESTNET_ARBITRUM]` and for production please use `Networks[MAINNET_ARBITRUM]`
​
​
```
from firefly_exchange_client import FireflyClient
from constants import Networks
from pprint import pprint
​
# initialize client
client = FireflyClient(
      True, # agree to terms and conditions
      Networks["TESTNET_ARBITRUM"], # network to connect with e.g. TESTNET_ARBITRUM | MAINNET_ARBITRUM
      "0x.....", # PK for the account
      True, # on boards user on firefly. Must be set to true for first time use
      )
​
print('Account Address:', client.get_public_address());
​
# # gets user account data on-chain
data = client.get_user_account_data()
​
pprint(data)
```
​
**Placing Orders:**
```
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from interfaces import OrderSignatureRequest
​
# initialize
client = FireflyClient(....) 
​
# creates a LIMIT order to be signed
signature_request = OrderSignatureRequest(
    symbol=MARKET_SYMBOLS.ETH,  # market symbol
    price=0,  # price at which you want to place order
    quantity=0.01, # quantity
    side=ORDER_SIDE.BUY, 
    orderType=ORDER_TYPE.MARKET,
    leverage=user_leverage
)  
​
# create signed order
signed_order = client.create_signed_order(signature_request);
​
print("Placing a market order")
# place signed order on orderbook
resp = client.post_signed_order(signed_order)
​
# returned order with PENDING state
print(resp)
```
​
**Listening To Events:**
```
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from interfaces import OrderSignatureRequest
​
def callback(event):
    print("Event data:", event)
​
# initialize
client = FireflyClient(....) 
​
# make connection with firefly exchange
client.socket.open()
​
# subscribe to local user events
client.socket.subscribe_user_update_by_token()
​
# listen to user order updates and trigger callback
client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)
​
#
# place some orders to exchange, that will trigger callback
# resp = client.post_signed_order(signed_order)
#
​
time.sleep(10)
​
# unsubscribe from user events
client.socket.unsubscribe_user_update_by_token()
​
# close socket connection
client.socket.close()
​
```
Look at [example](https://github.com/fireflyprotocol/firefly_exchange_client/tree/main/examples) directory to learn more about client usage.
