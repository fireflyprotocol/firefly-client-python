from config import TEST_ACCT_KEY, TEST_SUB_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from constants import Networks
from interfaces import OrderSignatureRequest

def main():

  # initialize client with parent account
  clientParent = FireflyClient(
        True, 
        Networks[TEST_NETWORK], 
        TEST_ACCT_KEY,
        True,
        )

  # initialize client with sub account key
  clientChild = FireflyClient(
        True,
        Networks[TEST_NETWORK], 
        TEST_SUB_ACCT_KEY, 
        True,
        )

  print("Parent: ", clientParent.get_public_address())

  print("Child: ", clientChild.get_public_address())

  # # whitelist sub account
  status = clientParent.update_sub_account(MARKET_SYMBOLS.ETH, clientChild.get_public_address(), True)
  print("Sub account created: {}".format(status))


  clientChild.add_market(MARKET_SYMBOLS.ETH)

  signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH, # sub account is only whitelisted for ETH market
        maker=clientParent.get_public_address(),  # maker of the order is the parent account
        price=0,  
        quantity=0.02,
        side=ORDER_SIDE.BUY, 
        orderType=ORDER_TYPE.MARKET,
        leverage=3,
    )  

  # order is signed using sub account's private key
  signed_order = clientChild.create_signed_order(signature_request);


  resp = clientChild.post_signed_order(signed_order)

  print(resp)

if __name__ == "__main__":
    main()