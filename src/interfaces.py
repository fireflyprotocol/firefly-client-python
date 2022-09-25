from typing import TypedDict
from enums import MARKET_SYMBOLS
from enums import ORDER_TYPE
from enums import ORDER_SIDE

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

class SignedOrder(Order):
    typedSignature: str

class RequiredOrderFields(TypedDict): 
  symbol: MARKET_SYMBOLS # market for which to create order
  price: int # price at which to place order. Will be zero for a market order
  quantity: int # quantity/size of order
  side: ORDER_SIDE # BUY/SELL
  orderType: ORDER_TYPE # MARKET/LIMIT


class OrderSignatureRequest(RequiredOrderFields): 
  leverage: int # (optional) leverage to take, default is 1
  reduceOnly: bool;# (optional)  is order to be reduce only true/false, default its false
  salt: int; # (optional)  random number for uniqueness of order. Generated randomly if not provided
  expiration: int; # (optional) time at which order will expire. Will be set to 1 month if not provided

class OrderSignatureResponse(RequiredOrderFields):
  orderSignature: str;
