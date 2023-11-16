import sys,os

from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import TIME_IN_FORCE,FireflyClient, Networks, MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE, OrderSignatureRequest, ORDER_STATUS
import asyncio



async def place_limit_order(client: FireflyClient):
   
    # default leverage of account is set to 3 on firefly
    user_leverage = await client.get_user_leverage(MARKET_SYMBOLS.ETH)

    # creates a LIMIT order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH,  # market symbol
        price=0,  # price at which you want to place order
        quantity=0.01, # quantity
        side=ORDER_SIDE.BUY, 
        orderType=ORDER_TYPE.STOP_MARKET,
        triggerPrice=1090.23,
        leverage=user_leverage,
        postOnly=False,
        cancelOnRevert=True,
        timeInForce=TIME_IN_FORCE.GOOD_TILL_TIME
    )  

   
    # create signed order
    signed_order = client.create_signed_order(signature_request)
    
    print (signed_order)


    print("Placing a limit order")
    # place signed order on orderbook
    resp = await client.post_signed_order(signed_order)

    # returned order
    print(resp)


    ## cancelling the stop orders
    cancellation_request = client.create_signed_cancel_orders(MARKET_SYMBOLS.ETH, order_hash=[resp['hash']])
    print(cancellation_request)

    
    # post order to exchange for cancellation
    resp = await client.post_cancel_order(cancellation_request)
    
    print(resp)

    # cancels all open orders, returns false if there is no open order to cancel
    resp = await client.cancel_all_orders(MARKET_SYMBOLS.ETH, [ORDER_STATUS.STAND_BY, ORDER_STATUS.STAND_BY_PENDING])
    print (resp)
    return



async def main():

    # initialize client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        )

    await client.init(True) 

    # add market that you wish to trade on ETH/BTC are supported currently
    client.add_market(MARKET_SYMBOLS.ETH)

    # await place_limit_order(client)
    await place_limit_order(client)
    
    await client.close_connections()


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
  loop.close()