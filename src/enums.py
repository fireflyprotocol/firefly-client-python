from enum import Enum

class ORDER_TYPE(Enum):
    LIMIT = "LIMIT",
    MARKET = "MARKET"

class ORDER_SIDE(Enum):
    BUY = "BUY",
    SELL = "SELL"

class MARKET_SYMBOLS(Enum):
    BTC = "BTC-PERP",
    ETH = "ETH-PERP",
    DOT = "DOT-PERP"
