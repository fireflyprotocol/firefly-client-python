# Firefly Client Library

[<img alt="Firefly logo" src="res/banner2.png" />](#)

Python client library to interact with firefly api gateway to place orders on firefly exchange and to interact with on-chain firefly contracts.
​
### How to use
The package can be installed from PyPI using pip:
```
pip install firefly-exchange-client
```

**Client initialization:**
When initializing the client, user must accept [terms and conditions](https://firefly.exchange/terms-of-use), provide a network object of type containing the following key/values:
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
User can import predefined networks from [constants](https://github.com/fireflyprotocol/firefly_exchange_client/blob/main/src/constants.py) like:
```
from constants import Networks
```
For testing purposes use `Networks[TESTNET_ARBITRUM]` and for prod use `Networks[MAINNET_ARBITRUM]`
​

Provide private key of the account used to sign the orders. **The key never leaves the client and is only used to sign transactions/orders off-chain.** The last argument is a boolean which must be passed as `True` when connecting the account specified by private key for the first time on firefly protocol. For future client initialization, this last flag can be passed as `False` as the account is already initialized.
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
      "0x.....", # private key of wallet
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