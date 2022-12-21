import socketio
from enumerations import MARKET_SYMBOLS, SOCKET_EVENTS

sio = socketio.Client()
      
class Sockets:
    callbacks={}
    def __init__(self,url,timeout=10) -> None:
        self.url = url   
        self.timeout = timeout
        return 

    def _establish_connection(self):
        """
            Connects to the desired url
        """
        try:
            sio.connect(self.url,wait_timeout=self.timeout)
            return True
        except:
            return False

    def open(self):
        """
            opens socket instance connection
        """
        self.connection_established = self._establish_connection()
        if not self.connection_established:
            self.close()
            raise(Exception("Failed to connect to Host: {}".format(self.url)))
        return
        

    def close(self):
        """
            closes the socket instance connection
        """
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
        except:
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
              
            sio.emit('UNSUBSCRIBE', [
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
            if not self.connection_established:
                return False
              
            sio.emit("SUBSCRIBE", [
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
            if not self.connection_established:
                return False
              
            sio.emit("UNSUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.UserUpdatesRoom.value[0],
                "u": user_address.lower(),
            },
            ])
            return True
        except:
            return False

    
  