###
# Places a market order on exchange and listens to emitted events
##
import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks,ORDER_STATUS, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest, SOCKET_EVENTS
import asyncio
event_received = False


async def main():

    client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
    await client.init(True)

    def callback(event):
        global event_received
        print(event)
        event_received = True

    async def connection_callback():
        # This callback will be invoked as soon as the socket connection is established
        # subscribe to local user events
        status = await client.socket.subscribe_user_update_by_token()
        print("Subscribed to user events: {}".format(status))

        # triggered when order updates are received
        print("Listening to user order updates")
        await client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)

    async def disconnection_callback():
        print("Sockets disconnected, performing actions...")
        resp =  await client.cancel_all_orders(MARKET_SYMBOLS.ETH, [ORDER_STATUS.OPEN, ORDER_STATUS.PARTIAL_FILLED])
        print(resp)

    # must specify connection_callback before opening the sockets below
    await client.socket.listen("connect", connection_callback)
    await client.socket.listen("disconnect", disconnection_callback)

    print("Making socket connection to firefly exchange")
    await client.socket.open()

    status = await client.socket.subscribe_user_update_by_token()
    print("Subscribed to user events: {}".format(status))

    ######## Placing an Order ########

    # add market that you wish to trade on
    client.add_market(MARKET_SYMBOLS.ETH)

    # default leverage of account is set to 3 on firefly
    user_leverage = await client.get_user_leverage(MARKET_SYMBOLS.ETH)

    # creates a MARKET order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH,
        leverage=user_leverage,
        price=0,
        quantity=0.5,
        side=ORDER_SIDE.BUY,
        orderType=ORDER_TYPE.MARKET
    )

    # create signed order
    signed_order = client.create_signed_order(signature_request)

    print("Placing a market order")
    # place signed order on orderbook
    resp = await client.post_signed_order(signed_order)

    ###### Closing socket connections after 30 seconds #####
    timeout = 30
    end_time = time.time() + timeout
    while not event_received and time.time() < end_time:
        time.sleep(1)

    # # close socket connection
    print("Closing sockets!")
    await client.socket.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()

