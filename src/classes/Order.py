from typing import TypedDict
from BigNumber import BigNumber

class Order(TypedDict):
    isBuy: bool
    reduceOnly: bool
    quantity: BigNumber
    price: BigNumber
    triggerPrice: BigNumber
    leverage: BigNumber
    maker: str
    taker: str
    expiration: BigNumber
    salt: BigNumber




    