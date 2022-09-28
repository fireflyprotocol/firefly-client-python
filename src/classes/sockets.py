import threading
import time
import socketio
import asyncio
from enums import MARKET_SYMBOLS, SOCKET_EVENTS

sio = socketio.AsyncClient()
      
class Sockets:
    callbacks={}
    def __init__(self,url,timeout=10) -> None:
        self.url = url   
        self.connection_established = False
        self.event_loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.event_loop)
        self.process = threading.Thread(target=self.create_socket_app) 
        self.process.start()
        max_time = time.time() + timeout
        while not self.connection_established and time.time() < max_time:
            pass
        if not self.connection_established:
            self.disconnect()
            raise Exception("Unable to connect to Host")
        return 

    async def account_stream_loop(self):
        """
            Connects to the desired url
        """
        try:
            await sio.connect(self.url)
            return True
        except Exception as e:
            print(e)
            return False

    def create_socket_app(self):
        """
            Creates an event loop that runs until stopped
        """
        try:
            def _connection_callback(x):
                if x.result() == True:
                    self.connection_established = True
                return 
            t = self.event_loop.create_task(self.account_stream_loop())
            t.add_done_callback(_connection_callback)
            self.event_loop.run_forever()
        except:
            pass
        return 

    async def disconnect_socket_app(self):
        await sio.disconnect()

    def disconnect(self):
        self.event_loop.create_task(self.disconnect_socket_app())
        self.event_loop.stop()
        self.process.join()
        return 

    @sio.on("*")
    def listener(event,data):
        """
            Listens to all events emitted by the server
        """
        try:
            if event in Sockets.callbacks.keys():
                Sockets.callbacks[event](data)
            elif "default" in Sockets.callbacks.keys():
                Sockets.callbacks["default"]({"event":event,"data":data})
            else:
                pass
        except:
            pass
        return 

    async def emit(self,action,value):
        """
            Makes an emit for the client 
            Inputs:
                - action: The action to be performed (e.g. SUBSCRIBE)
                - value: the required paramenters for the action (e.g. A required subscription key)
        """
        await sio.emit(action, value)
        return 

    def listen(self,event,callback):
        """
            Assigns callbacks to desired events
        """
        Sockets.callbacks[event] = callback
        return 

    def subscribe_global_updates_by_symbol(self,symbol: MARKET_SYMBOLS):
        """
            Allows user to subscribe to global updates for the desired symbol.
            Inputs:
                - symbol: market symbol of market user wants global updates for. (e.g. DOT-PERP)
        """
        try:
            if not self.connection_established:
                return False 
            self.event_loop.create_task(self.emit('SUBSCRIBE',[
            {
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
                "p": symbol.value,
            },
            ]))
            return True
        except Exception as e:
            print(e)
            return False

    def unsubscribe_global_updates_by_symbol(self,symbol: MARKET_SYMBOLS):
        """
            Allows user to unsubscribe to global updates for the desired symbol.
                Inputs:
                    - symbol: market symbol of market user wants to remove global updates for. (e.g. DOT-PERP)
        """
        try:
            if not self.connection_established:
                return False 
            self.event_loop.run_until_complete(self.emit('UNSUBSCRIBE', [
            {
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
                "p": symbol.value,
            },
            ]))
            return True
        except:
            return False

    def subscribe_user_update_by_address(self,user_address: str):
        """
            Allows user to subscribe to their accout updates.
            Inputs:
                - user_address: user address(Public Key) of the user. (e.g. 0x000000000000000000000000)
        """
        try:
            self.event_loop.run_until_complete(self.emit("SUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.UserUpdatesRoom,
                "u": user_address.lower(),
            },
            ]))
            return True
        except:
            return False

    def unsubscribe_user_update_by_address(self,user_address:str): 
        """
            Allows user to unsubscribe to their accout updates.
            Inputs:
                - user_address: user address(Public Key) of the user. (e.g. 0x000000000000000000000000)
        """
        try:
            self.event_loop.run_until_complete(self.emit("UNSUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.UserUpdatesRoom,
                "u": user_address.lower(),
            },
            ]))
            return True
        except:
            return False

    
  