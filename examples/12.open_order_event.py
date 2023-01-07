'''
The code example opens socket connection and listens to user order update events
It places a limit order and as soon as its OPENED on order book, we receive
an event, log its data and terminate connection
'''
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, SOCKET_EVENTS
from interfaces import OrderSignatureRequest
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE

client:FireflyClient = FireflyClient(
    True, # agree to terms and conditions
    Networks[TEST_NETWORK], # network to connect with
    TEST_ACCT_KEY, # private key of wallet
    True, # on boards user on firefly. Must be set to true for first time use
    )

client.add_market(MARKET_SYMBOLS.ETH)

def callback(event):
    print("Event data:", event)
    
    status = client.socket.unsubscribe_user_update_by_token()
    print("Unsubscribed from user events: {}".format(status))

    # close socket connection
    print("Closing sockets!")
    client.socket.close()

def place_limit_order():
       
    # default leverage of account is set to 3 on firefly
    user_leverage = client.get_user_leverage(MARKET_SYMBOLS.ETH)

    # creates a LIMIT order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH,  # market symbol
        price=1300,  # price at which you want to place order
        quantity=0.01, # quantity
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.LIMIT,
        leverage=user_leverage
    )  

    # create signed order
    signed_order = client.create_signed_order(signature_request);

    print("Placing a limit order")
    # place signed order on orderbook
    resp = client.post_signed_order(signed_order)

    # returned order with PENDING state
    print(resp)

    return


# must open socket before subscribing
print("Making socket connection to firefly exchange")
client.socket.open()

# subscribe to user events 
client.socket.subscribe_user_update_by_token()
print("Subscribed to user events")

print("Listening to user order updates")
client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)


place_limit_order()
