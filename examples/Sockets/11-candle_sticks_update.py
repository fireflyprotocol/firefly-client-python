###
# Places a market order on exchange and listens to emitted events
##
import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest, SOCKET_EVENTS
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
        # subscribe to global event updates for BTC market
        status = await client.socket.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.ETH)
        print("Subscribed to global ETH events: {}".format(status))

        # triggered when account data updates are received
        print("Listening to candle stick updates")
        await client.socket.listen(SOCKET_EVENTS.GET_LAST_KLINE_WITH_INTERVAL, callback)

    async def disconnection_callback():
        print("Sockets disconnected, performing actions...")

    # must specify connection_callback before opening the sockets below
    await client.socket.listen("connect", connection_callback)
    await client.socket.listen("disconnect", disconnection_callback)

    print("Making socket connection to firefly exchange")
    await client.socket.open()

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
   ### make sure keep the loop initialization same 
    # as below to ensure closing the script after receiving 
    # completion of each callback on socket events ###  
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    pending = asyncio.all_tasks(loop=loop)
    group = asyncio.gather(*pending)
    loop.run_until_complete(group)

