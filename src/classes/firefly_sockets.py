import threading
import socketio
import asyncio
from utils import get_or_create_eventloop 
from enums import MARKET_SYMBOLS, SOCKET_EVENTS
sio = socketio.AsyncClient()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
      
class Sockets:
    def __init__(self,url) -> None:
        self.url = url   
        self.process = threading.Thread(target=self.create_order_socket)    
        self.process.start()
        return 

    async def account_stream_loop(self):
        await sio.connect(self.url)
                
    def create_order_socket(self):
        try:
            asyncio.set_event_loop(get_or_create_eventloop())
            get_or_create_eventloop().run_until_complete(self.account_stream_loop())
            get_or_create_eventloop().run_forever()
        except Exception as e:
            lmsg = "FireflyUserListener: create_order_socket, Exception:{}".format(e)
            print(lmsg)
        return 


    @sio.on("*")
    def listener(event,data):
        print(event,data)

    def callback(self,**kwargs):
        print(kwargs)
        return

    async def emit(self,action,value):
        await sio.emit(action, value)
    

    def subscribe_global_updates_by_symbol(self,symbol: MARKET_SYMBOLS):
        get_or_create_eventloop().run_until_complete(self.emit('SUBSCRIBE',[
        {
            "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
            "p": symbol.value,
        },
        ]))
        return True

    def unsubscribe_global_updates_by_symbol(self,symbol: MARKET_SYMBOLS):
        get_or_create_eventloop().run_until_complete('UNSUBSCRIBE', [
        {
            "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
            "p": symbol.value,
        },
        ])
        return True

    def subscribe_user_update_by_address(user_address: str):
        get_or_create_eventloop().run_until_complete("SUBSCRIBE", [
        {
            "e": SOCKET_EVENTS.UserUpdatesRoom,
            "u": user_address.lower(),
        },
        ])
        return True

    def unsubscribe_user_update_by_address(user_address:str): 
        get_or_create_eventloop().run_until_complete("UNSUBSCRIBE", [
        {
            "e": SOCKET_EVENTS.UserUpdatesRoom,
            "u": user_address.lower(),
        },
        ])
        return True
  