# Firefly Client Library
[<img alt="Firefly logo" src="https://raw.githubusercontent.com/fireflyprotocol/firefly_exchange_client/main/res/banner.png" />](#)

<div align="center">

![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/fireflyprotocol/firefly_exchange_client/publish_to_pypi.yml)
[![pypi version](https://img.shields.io/pypi/v/firefly_exchange_client?logo=pypi)](https://pypi.org/project/firefly_exchange_client/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
</div>



Python Client for the Firefly Exchange API and Smart Contracts.
​
### Install
The package can be installed from [PyPi](https://pypi.org/project/firefly-exchange-client/) using pip:
```
pip install firefly-exchange-client
```
The package currently supports python `>=3.8`. Find complete documentation on the library at https://docs.firefly.exchange/.

### Getting Started

When initializing the client, users must accept [terms and conditions](https://firefly.exchange/terms-of-use) and define network object containing the following values:
```json
{
    "url": "https://goerli-rollup.arbitrum.io/rpc",
    "chainId": 421613,
    "apiGateway": "https://dapi-testnet.firefly.exchange",
    "socketURL": "wss://dapi-testnet.firefly.exchange",
    "webSocketURL": "",
    "onboardingUrl": "https://testnet.firefly.exchange",
},
```
Users can import predefined networks from [constants](https://github.com/fireflyprotocol/firefly_exchange_client/blob/main/src/firefly_exchange_client/constants.py):
```python
from firefly_exchange_client import Networks
```
For testing purposes use `Networks[TESTNET_ARBITRUM]` and for production please use `Networks[MAINNET_ARBITRUM]`
​
​
```python
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
  await client.init(True) 
  
  print('Account Address:', client.get_public_address());

  # # gets user account data on-chain
  data = await client.get_user_account_data()

  # close aio http connection
  await client.apis.close_session()

  pprint(data)

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
```
​
**Placing Orders:**
```python
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest
​import asyncio

# initialize
client = FireflyClient(....) 
​client.init(True)

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
resp = await client.post_signed_order(signed_order)
​
# returned order with PENDING state
print(resp)
```
​
**Listening To Events Using Socket.io:**
```python
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest
​
def callback(event):
    print("Event data:", event)
​
# initialize
client = FireflyClient(....) 
​client.init(True)

# make connection with firefly exchange
await client.socket.open()
​
# subscribe to local user events
await client.socket.subscribe_user_update_by_token()
​
# listen to user order updates and trigger callback
await client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)
​
#
# place some orders to exchange, that will trigger callback
# resp = client.post_signed_order(signed_order)
#
​
time.sleep(10)
​
# unsubscribe from user events
await client.socket.unsubscribe_user_update_by_token()
​
# close socket connection
await client.socket.close()
​
```
Look at the [example](https://github.com/fireflyprotocol/firefly_exchange_client/tree/main/examples) directory to see more examples on how to use this library.

**Listening To Events Using Web Sockets:**
```python
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, SOCKET_EVENTS, OrderSignatureRequest
import time
def callback(event):
    print("Event data:", event)

# initialize
client = FireflyClient(....) 
client.init()

# make connection with firefly exchange
client.webSocketClient.initialize_socket(on_open=on_open)


def on_open(ws):
  # subscribe to local user events
  client.webSocketClient.subscribe_user_update_by_token()
  
  # listen to user order updates and trigger callback
  client.webSocketClient.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)
  #
  # place some orders to exchange, that will trigger callback
  # resp = client.post_signed_order(signed_order)
  #
  time.sleep(10)

  # unsubscribe from user events
  client.webSocketClient.unsubscribe_user_update_by_token()

  # close socket connection
  client.webSocketClient.stop()
```