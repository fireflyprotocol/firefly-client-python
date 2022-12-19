from typing import TypedDict
from enumerations import *

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

class OrderResponse(TypedDict):
  id: int
  clientId: str
  requestTime: int
  cancelReason: CANCEL_REASON
  orderStatus: ORDER_STATUS
  hash: str
  symbol: MARKET_SYMBOLS
  orderType: ORDER_TYPE
  timeInForce: TIME_IN_FORCE
  userAddress: str
  side: ORDER_SIDE
  price: str
  quantity: str
  leverage: str
  reduceOnly: bool
  expiration: int
  salt: int
  orderSignature: str
  filledQty: str
  avgFillPrice: str
  createdAt: int
  updatedAt: int
  makerFee: str
  takerFee: str
  openQty: str
  cancelOnRevert: bool


class GetOrderResponse(OrderResponse):
  fee: str
  postOnly: bool
  triggerPrice: str


class GetCandleStickRequest(TypedDict):
  symbol: MARKET_SYMBOLS
  interval: Interval
  startTime: float
  endTime: float
  limit: int

class GetMarketRecentTradesRequest(TypedDict):
  symbol: MARKET_SYMBOLS
  pageSize: int
  pageNumber: int
  traders: TRADE_TYPE

class OrderCancelSignatureRequest(TypedDict):
  symbol: MARKET_SYMBOLS
  hashes: list

class OrderCancellationRequest(OrderCancelSignatureRequest):
  signature: str

class CancelOrder(TypedDict):
  hash: str
  reason: str


class CancelOrderResponse(TypedDict):
  message: str
  data: dict


class GetTransactionHistoryRequest(TypedDict):
  symbol: MARKET_SYMBOLS  # will fetch orders of provided market
  pageSize: int  # will get only provided number of orders must be <= 50
  pageNumber: int  # will fetch particular page records. A single page contains 50 records.

class GetPositionRequest(TypedDict):
  symbol: MARKET_SYMBOLS  # will fetch orders of provided market
  pageSize: int  # will get only provided number of orders must be <= 50
  pageNumber: int  # will fetch particular page records. A single page contains 50 records.

class GetUserTradesRequest(TypedDict):
  symbol: MARKET_SYMBOLS
  maker: bool
  fromId: int
  startTime: int
  endTime: int
  pageSize: int
  pageNumber: int
  type: ORDER_TYPE

class GetOrderRequest(GetTransactionHistoryRequest):
  statuses:ORDER_STATUS # status of orders to be fetched


