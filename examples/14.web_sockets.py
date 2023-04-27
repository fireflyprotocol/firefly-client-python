import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient, Networks, MARKET_SYMBOLS, SOCKET_EVENTS, config_logging
import asyncio
import logging

config_logging(logging, logging.DEBUG)

def callback(event):
    print("Event data:", event)

async def main():
   client = FireflyClient(True, Networks[TEST_NETWORK], TEST_ACCT_KEY)
   await client.init(True)
   
   def on_error(ws, error):
        print(error)
        
   def on_close(ws, close_status_code, close_msg):
        print("### closed ###")
    
   def on_open(ws):
        # subscribe to global event updates for BTC market 
        status = client.webSocketClient.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
        print("Subscribed to global BTC events: {}".format(status))

        # subscribe to local user events
        client.webSocketClient.subscribe_user_update_by_token()
        print("Subscribed to user events")

        # triggered when order book updates
        print("Listening to Orderbook updates")
        client.webSocketClient.listen(SOCKET_EVENTS.ORDERBOOK_UPDATE.value, callback)

        # triggered when status of any user order updates
        print("Listening to user order updates")
        client.webSocketClient.listen(SOCKET_EVENTS.ORDER_UPDATE.value, callback)

        # SOCKET_EVENTS contains all events that can be listened to
        
        # logs event name and data for all markets and users that are subscribed.
        # helpful for debugging
        # client.socket.listen("default",callback)

        time.sleep(60)
        # unsubscribe from global events
        status = client.webSocketClient.unsubscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
        print("Unsubscribed from global BTC events: {}".format(status))

        status = client.webSocketClient.unsubscribe_user_update_by_token()
        print("Unsubscribed from user events: {}".format(status))


        # close socket connection
        print("Closing sockets!")
        client.webSocketClient.stop()

    
   print("Making socket connection to firefly exchange")
   client.webSocketClient.initialize_socket(on_open=on_open, on_error=on_error,on_close=on_close)
   
   await client.apis.close_session() 

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())