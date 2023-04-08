import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, SOCKET_EVENTS
import asyncio

def callback(event):
    print("Event data:", event)

async def main():

  client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
  await client.init(True)

  # must open socket before subscribing
  print("Making socket connection to firefly exchange")
  await client.socket.open()

  # subscribe to global event updates for BTC market 
  status = await client.socket.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
  print("Subscribed to global BTC events: {}".format(status))

  # subscribe to local user events
  status = await client.socket.subscribe_user_update_by_token()
  print("Subscribed to user events: {}".format(status))

  # triggered when order book updates
  print("Listening to Orderbook updates")
  await client.socket.listen(SOCKET_EVENTS.ORDERBOOK_UPDATE.value, callback)

  # triggered when status of any user order updates
  print("Listening to user order updates")
  await client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)

  # SOCKET_EVENTS contains all events that can be listened to
  
  # logs event name and data for all markets and users that are subscribed.
  # helpful for debugging
  # client.socket.listen("default",callback)

  time.sleep(60)
  # unsubscribe from global events
  status = await client.socket.unsubscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
  print("Unsubscribed from global BTC events: {}".format(status))

  status = await client.socket.unsubscribe_user_update_by_token()
  print("Unsubscribed from user events: {}".format(status))


  # close socket connection
  print("Closing sockets!")
  await client.socket.close()

  await client.apis.close_session();



if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())