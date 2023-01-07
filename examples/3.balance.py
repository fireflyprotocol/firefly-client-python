from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
import asyncio

async def main():

  # initialize client
  client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

  # checks chain native token balance.
  # A user must have native tokens to perform contract calls
  print('Chain token balance:', await client.get_native_chain_token_balance());

  # check margin bank balance on-chain
  print('Margin bank balance:', await client.get_margin_bank_balance());

  # check usdc balance user has on-chain
  print('USDC balance:', await client.get_usdc_balance());  

  # deposit usdc to margin bank
  # must have native chain tokens to pay for gas fee
  print('USDC deposited:', await client.deposit_margin_to_bank(10));

  # check margin bank balance
  print('Margin bank balance:', await client.get_margin_bank_balance());

  # check margin bank balance
  print('USDC Withdrawn:', await client.withdraw_margin_from_bank(5));

  # check margin bank balance
  print('Margin bank balance:', await client.get_margin_bank_balance());

if __name__ == "__main__":
    asyncio.run(main())