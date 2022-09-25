from typing import TypedDict
from enums import *

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
  reduceOnly: bool # (optional)  is order to be reduce only true/false, default its false
  salt: int # (optional)  random number for uniqueness of order. Generated randomly if not provided
  expiration: int # (optional) time at which order will expire. Will be set to 1 month if not provided

class OrderSignatureResponse(RequiredOrderFields):
  orderSignature: str

class PlaceOrderRequest(OrderSignatureResponse):
  timeInForce: TIME_IN_FORCE # FOK/IOC/GTT by default all orders are GTT
  postOnly: bool # true/false, default is true
  clientId: str # id of the client

class GetOrderbookRequest(TypedDict):
  symbol: str
  limit: int # number of bids/asks to retrieve, should be <= 50

class OnboardingMessage(TypedDict):
    action: str
    onlySignOn: str

