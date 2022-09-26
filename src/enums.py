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

class TIME_IN_FORCE(Enum):
    FILL_OR_KILL = "FOK",
    IMMEDIATE_OR_CANCEL = "IOC",
    GOOD_TILL_TIME = "GTT"

class ONBOARDING_MESSAGES(Enum):
    ONBOARDING = "Firefly Onboarding",
    KEY_DERIVATION = "Firefly Access Key"

class ORDER_STATUS(Enum): 
    PENDING = "PENDING",
    OPEN = "OPEN",
    PARTIAL_FILLED = "PARTIAL_FILLED",
    FILLED = "FILLED",
    CANCELLING = "CANCELLING",
    CANCELLED = "CANCELLED",
    REJECTED = "REJECTED",
    EXPIRED = "EXPIRED"

class CANCEL_REASON(Enum):
    UNDERCOLLATERALIZED = "UNDERCOLLATERALIZED",
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE",
    USER_CANCELLED = "USER_CANCELLED",
    EXCEEDS_MARKET_BOUND = "EXCEEDS_MARKET_BOUND",
    COULD_NOT_FILL = "COULD_NOT_FILL",
    EXPIRED = "EXPIRED",
    USER_CANCELLED_ON_CHAIN = "USER_CANCELLED_ON_CHAIN",
    SYSTEM_CANCELLED = "SYSTEM_CANCELLED",
    SELF_TRADE = "SELF_TRADE",
    POST_ONLY_FAIL = "POST_ONLY_FAIL",
    FAILED = "FAILED",
    NETWORK_DOWN = "NETWORK_DOWN"

class Interval(Enum):
    _1m = "1m" 
    _3m = "3m" 
    _5m = "5m" 
    _15m = "15m" 
    _30m = "30m" 
    _1h = "1h" 
    _2h = "2h" 
    _4h = "4h" 
    _6h = "6h" 
    _8h = "8h" 
    _12h = "12h" 
    _1d = "1d" 
    _3d = "3d" 
    _1w = "1w" 
    _1M = "1M"


