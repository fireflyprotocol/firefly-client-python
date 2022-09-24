from typing import TypedDict

class Order(TypedDict):
    isBuy: bool 
    reduceOnly: bool 
    quantity: int 
    price: int 
    triggerPrice: int 
    leverage: int 
    expiration: int 
    salt: int   
    maker: str 
    taker:str