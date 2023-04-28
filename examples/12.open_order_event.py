'''
The code example opens socket connection and listens to user order update events
It places a limit order and as soon as its OPENED on order book, we receive
an event, log its data and terminate connection
'''
import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, SOCKET_EVENTS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest
import asyncio





async def place_limit_order(client:FireflyClient):
       
    # default leverage of account is set to 3 on firefly
    user_leverage = await client.get_user_leverage(MARKET_SYMBOLS.ETH)

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
    signed_order = client.create_signed_order(signature_request) 

    print("Placing a limit order")
    # place signed order on orderbook
    resp = await client.post_signed_order(signed_order)

    # returned order with PENDING state
    print(resp)

    return


async def main():

    client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
    await client.init(True)

    client.add_market(MARKET_SYMBOLS.ETH)

    def callback(event):
        print("Event data:", event)

    # must open socket before subscribing
    print("Making socket connection to firefly exchange")
    await client.socket.open()

    # subscribe to user events 
    await client.socket.subscribe_user_update_by_token()
    print("Subscribed to user events")

    print("Listening to user order updates")
    await client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)
    
    # place a limit order
    await place_limit_order(client)
    time.sleep(3)
    status = await client.socket.unsubscribe_user_update_by_token()
    print("Unsubscribed from user events: {}".format(status))

    # close socket connection
    print("Closing sockets!")
    await client.socket.close()

    await client.apis.close_session() 



if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()

