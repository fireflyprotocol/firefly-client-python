import socketio
from .enumerations import MARKET_SYMBOLS, SOCKET_EVENTS

sio = socketio.Client()
      
class Sockets:
    callbacks={}
    def __init__(self, url:str, timeout:int=10, token:str=None) -> None:
        self.url = url  
        self.timeout = timeout
        self.token = token
        return 

    def _establish_connection(self) -> bool:
        """
            Connects to the desired url
        """
        try:
            sio.connect(self.url,wait_timeout=self.timeout,transports=["websocket"])
            return True
        except:
            return False

    def set_token(self, token) -> None:
        """
            Sets default user token
            Inputs:
                - token (user auth token): firefly onboarding token.
        """
        self.token = token

    async def open(self) -> None:
        """
            opens socket instance connection
        """
        self.connection_established = self._establish_connection()
        if not self.connection_established:
            self.close()
            raise(Exception("Failed to connect to Host: {}".format(self.url)))
        return
        

    async def close(self) -> None:
        """
            closes the socket instance connection
        """
        sio.disconnect()
        return 

    @sio.on("*")
    def listener(event,data) -> None:
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

    async def listen(self, event:str, callback) -> None:
        """
            Assigns callbacks to desired events
        """
        Sockets.callbacks[event] = callback
        return 

    async def subscribe_global_updates_by_symbol(self, symbol: MARKET_SYMBOLS) -> bool:
        """
            Allows user to subscribe to global updates for the desired symbol.
            Inputs:
                - symbol: market symbol of market user wants global updates for. (e.g. DOT-PERP)
        """
        try:
            if not self.connection_established:
                raise Exception("Socket connection is established, invoke socket.open()")

            sio.emit('SUBSCRIBE',[
            {
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
                "p": symbol.value,
            },
            ])
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    async def unsubscribe_global_updates_by_symbol(self,symbol: MARKET_SYMBOLS) -> bool:
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
                "e": SOCKET_EVENTS.GLOBAL_UPDATES_ROOM.value,
                "p": symbol.value,
            },
            ])
            return True
        except:
            return False

    async def subscribe_user_update_by_token(self, parent_account:str=None, user_token: str=None) -> bool:
        """
            Allows user to subscribe to their account updates.
            Inputs:
                - parent_account(str): address of parent account. Only whitelisted 
                  sub-account can listen to its parent account position updates
                - user_token(str): auth token generated when onboarding on firefly
        """
        try:
            if not self.connection_established:
                return False
              
            sio.emit("SUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.USER_UPDATES_ROOM.value,
                'pa': parent_account,
                "t": user_token or self.token,
            },
            ])
            return True
        except Exception as e:
            print(e);
            return False

    async def unsubscribe_user_update_by_token(self, parent_account:str=None, user_token:str=None) -> bool: 
        """
            Allows user to unsubscribe to their account updates.
            Inputs:
                - parent_account: address of parent account. Only for sub-accounts
                - user_token: auth token generated when onboarding on firefly
        """
        try:
            if not self.connection_established:
                return False
              
            sio.emit("UNSUBSCRIBE", [
            {
                "e": SOCKET_EVENTS.USER_UPDATES_ROOM.value,
                'pa': parent_account,
                "t": user_token or self.token,
            },
            ])
            return True
        except:
            return False

    
  