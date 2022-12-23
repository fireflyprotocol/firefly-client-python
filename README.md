# Firefly Client Library - Python
Python client library to interact with firefly api gateway to place orders on firefly exchange and to interact with on-chain firefly contracts.

### How to use

**Client initialization:**
```
from firefly_exchange_client import FireflyClient
from constants import Networks
from pprint import pprint

# initialize client
client = FireflyClient(
      True, # agree to terms and conditions
      Networks["TESTNET_ARBITRUM"], # network to connect with e.g. TESTNET_ARBITRUM | MAINNET_ARBITRUM
      "0x.....", # private key of wallet
      True, # on boards user on firefly. Must be set to true for first time use
      )

print('Account Address:', client.get_public_address());

# # gets user account data on-chain
data = client.get_user_account_data()

pprint(data)

```

**Placing Orders:**
```
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from interfaces import OrderSignatureRequest

# initialize
client = FireflyClient(....) 

# creates a LIMIT order to be signed
signature_request = OrderSignatureRequest(
    symbol=MARKET_SYMBOLS.ETH,  # market symbol
    price=0,  # price at which you want to place order
    quantity=0.01, # quantity
    side=ORDER_SIDE.BUY, 
    orderType=ORDER_TYPE.MARKET,
    leverage=user_leverage
)  

# create signed order
signed_order = client.create_signed_order(signature_request);

print("Placing a market order")
# place signed order on orderbook
resp = client.post_signed_order(signed_order)

# returned order with PENDING state
print(resp)

```

**Listening To Events:**
```

from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from interfaces import OrderSignatureRequest

def callback(event):
    print("Event data:", event)

# initialize
client = FireflyClient(....) 

# make connection with firefly exchange
client.socket.open()

# subscribe to local user events
client.socket.subscribe_user_update_by_token()

# listen to user order updates and trigger callback
client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)

#
# place some orders to exchange, that will trigger callback
# resp = client.post_signed_order(signed_order)
#

time.sleep(10)

# unsubscribe from user events
client.socket.unsubscribe_user_update_by_token()

# close socket connection
client.socket.close()

```


Look at [example](https://github.com/fireflyprotocol/firefly_exchange_client/tree/main/examples) directory to learn more about client usage.