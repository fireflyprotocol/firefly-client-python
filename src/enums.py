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

class SOCKET_EVENTS(Enum):
    GET_LAST_KLINE_WITH_INTERVAL = "{symbol}@kline@{interval}",
    GLOBAL_UPDATES_ROOM = "globalUpdates",
    GlobalUpdatesRoom = "globalUpdates",
    MarketDataUpdateKey = "MarketDataUpdate",
    RecentTradesKey = "RecentTrades",
    OrderbookUpdateKey = "OrderbookUpdate",
    AdjustMarginKey = "AdjustMargin",
    MarketHealthKey = "MarketHealth",
    ExchangeHealthKey = "ExchangeHealth",
    UserUpdatesRoom = "userUpdates",
    OrderUpdateKey = "OrderUpdate",
    OrderCancelledKey = "OrderCancelled",
    PositionUpdateKey = "PositionUpdate",
    UserTradeKey = "UserTrade",
    UserTransaction = "UserTransaction",
    AccountDataUpdateKey = "AccountDataUpdate"
