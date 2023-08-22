###
# Places a market order on exchange and listens to emitted events
##
import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, SOCKET_EVENTS
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
        # triggered when exchange health updates are received
        print("Listening to exchange health updates")
        await client.socket.listen(SOCKET_EVENTS.EXCHANGE_HEALTH.value, callback)

    async def disconnection_callback():
        print("Sockets disconnected, performing actions...")

    # must specify connection_callback before opening the sockets below
    await client.socket.listen("connect", connection_callback)
    await client.socket.listen("disconnect", disconnection_callback)

    print("Making socket connection to firefly exchange")
    await client.socket.open()

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


