from logging import raiseExceptions
from socket import SocketIO
import threading
import time
import socketio
import asyncio
from enums import MARKET_SYMBOLS, SOCKET_EVENTS

sio = socketio.Client()
      
class Sockets:
    callbacks={}
    def __init__(self,url,timeout=15) -> None:
        self.url = url   
        self.connection_established = self.establish_connection()
        if not self.connection_established:
            self.disconnect()
            raise(Exception("Failed to connect to Host: {}".format(self.url)))
        return 

    def establish_connection(self):
        """
            Connects to the desired url
        """
        try:
            sio.connect(self.url)
            return True
        except Exception as e:
            print(e)
            return False

    def disconnect(self):
        sio.disconnect()
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

    def emit(self,action,value):
        """
            Makes an emit for the client 
            Inputs:
                - action: The action to be performed (e.g. SUBSCRIBE)
                - value: the required paramenters for the action (e.g. A required subscription key)
        """
        sio.emit(action, value)
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
            sio.emit('SUBSCRIBE',[
            {
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value[0],
                "p": symbol.value,
            },
            ])
            
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
            self.emit('UNSUBSCRIBE', [
            {
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value[0],
                "p": symbol.value,
            },
            ])
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
            self.emit("SUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.UserUpdatesRoom.value[0],
                "u": user_address.lower(),
            },
            ])
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
            self.emit("UNSUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.UserUpdatesRoom.value[0],
                "u": user_address.lower(),
            },
            ])
            return True
        except:
            return False

    
  