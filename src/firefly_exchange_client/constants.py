Networks = {
  "TESTNET_ARBITRUM": {
    "url": "https://goerli-rollup.arbitrum.io/rpc",
    "chainId": 421613,
    "apiGateway": "https://dapi.api.arbitrum-staging.firefly.exchange",
    "dmsURL": "https://api.arbitrum-staging.firefly.exchange/dead-man-switch",
    "socketURL": "wss://dapi.api.arbitrum-staging.firefly.exchange",
    "webSocketURL": "wss://notifications.api.arbitrum-staging.firefly.exchange",
    "onboardingUrl": "https://testnet.firefly.exchange",
    "UUID": ""
  },
  "MAINNET_ARBITRUM": {
    "url": "https://arb1.arbitrum.io/rpc/",
    "chainId": 42161,
    "apiGateway": "https://dapi.api.arbitrum-prod.firefly.exchange",
    "dmsURL": "https://api.arbitrum-prod.firefly.exchange/dead-man-switch",
    "socketURL": "wss://dapi.api.arbitrum-prod.firefly.exchange",
    "webSocketURL": "wss://notifications.api.arbitrum-prod.firefly.exchange",
    "onboardingUrl": "https://trade-arb.firefly.exchange",
    "UUID": ""
  },
  "MAINNET_ARBITRUM_INTERNAL": {
    "url": "https://arb1.arbitrum.io/rpc/",
    "chainId": 42161,
    "apiGateway": "https://dapi.api.arbitrum-prod.int.firefly.exchange",
    "dmsURL": "https://api.arbitrum-prod.int.firefly.exchange/dead-man-switch",
    "socketURL": "wss://dapi.api.arbitrum-prod.int.firefly.exchange",
    "webSocketURL": "wss://notifications.api.arbitrum-prod.int.firefly.exchange",
    "onboardingUrl": "https://trade-arb.firefly.exchange",
    "UUID": ""
  }
}


EIP712_DOMAIN_NAME = "IsolatedTrader"


EIP712_DOMAIN_STRING = "EIP712Domain(string name,string version,uint128 chainId,address verifyingContract)"


EIP712_ORDER_STRUCT_STRING = \
    "Order(" +  \
    "bytes8 flags," + \
    "uint128 quantity," + \
    "uint128 price," + \
    "uint128 triggerPrice," + \
    "uint128 leverage," + \
    "address maker," + \
    "uint128 expiration" + \
    ")"

ORDER_FLAGS = {
    "IS_BUY":1,
    "IS_DECREASE_ONLY": 2
}

TIME = {
  "SECONDS_IN_A_MINUTE": 60,
  "SECONDS_IN_A_DAY": 86400,
  "SECONDS_IN_A_MONTH": 2592000
}

ADDRESSES = {
  "ZERO": "0x0000000000000000000000000000000000000000",
}

SERVICE_URLS = {
  "MARKET": {
    "ORDER_BOOK": "/orderbook",
    "RECENT_TRADE": "/recentTrades",
    "CANDLE_STICK_DATA": "/candlestickData",
    "EXCHANGE_INFO": "/exchangeInfo",
    "MARKET_DATA": "/marketData",
    "META": "/meta",
    "STATUS": "/status",
    "SYMBOLS": "/marketData/symbols",
    "CONTRACT_ADDRESSES": "/marketData/contractAddresses",
    "TICKER": "/ticker",
    "MASTER_INFO": "/masterInfo",
    "FUNDING_RATE":"/fundingRate"
  },
  "USER": {
    "USER_POSITIONS": "/userPosition",
    "USER_TRADES": "/userTrades",
    "ORDERS": "/orders",
    "ORDERS_BY_TYPE": "/orders/by-order-type",
    "GENERATE_READONLY_TOKEN": "/generateReadOnlyToken",
    "ACCOUNT": "/account",
    "USER_TRANSACTION_HISTORY": "/userTransactionHistory",
    "AUTHORIZE": "/authorize",
    "ADJUST_LEVERAGE": "/account/adjustLeverage",
    "FUND_GAS": "/account/fundGas",
    "TRANSFER_HISTORY": "/userTransferHistory",
    "FUNDING_HISTORY": "/userFundingHistory",
    "CANCEL_ON_DISCONNECT": "/dms-countdown",
     "USER_TRADES_HISTORY": "/userTradesHistory",
  },
  "ORDERS": {
    "ORDERS": "/orders",
    "ORDERS_HASH": "/orders/hash",
  },
  "GROWTH": {
    "REFERRER_INFO": "/growth/getReferrerInfo",
    "CAMPAIGN_DETAILS": "/growth/campaignDetails",
    "CAMPAIGN_REWARDS": "/growth/campaignRewards",
    "AFFILIATE_PAYOUTS": "/growth/affiliate/payouts",
    "AFFILIATE_REFEREE_DETAILS": "/growth/affiliate/refereeDetails",
    "AFFILIATE_REFEREES_COUNT": "/growth/affiliate/refereesCount",
    "USER_REWARDS_HISTORY": "/growth/userRewards/history",
    "USER_REWARDS_SUMMARY": "/growth/userRewards/summary",
    "REWARDS_OVERVIEW": "/growth/tradeAndEarn/rewardsOverview",
    "REWARDS_DETAILS": "/growth/tradeAndEarn/rewardsDetail",
    "TOTAL_HISTORICAL_TRADING_REWARDS": "/growth/tradeAndEarn/totalHistoricalTradingRewards",
    "MAKER_REWARDS_SUMMARY": "/growth/marketMaker/maker-rewards-summary",
    "MAKER_REWARDS_DETAILS": "/growth/marketMaker/maker-rewards-detail",
    "MAKER_WHITELIST_STATUS": "/growth/marketMaker/whitelist-status",
    "GENERATE_CODE": "/growth/generateCode",
    "LINK_REFERRED_USER": "/growth/linkReferredUser"
  },
}

EIP712_CANCEL_ORDER_STRUCT_STRING ="CancelLimitOrder(string action,bytes32[] orderHashes)"

EIP712_ONBOARDING_ACTION_STRUCT_STRING = \
    'firefly(' + \
    'string action,' + \
    'string onlySignOn' + \
    ')'

EIP712_DOMAIN_STRING_NO_CONTRACT = \
    "EIP712Domain(" + \
    "string name," + \
    "string version," + \
    "uint128 chainId" + \
    ")"