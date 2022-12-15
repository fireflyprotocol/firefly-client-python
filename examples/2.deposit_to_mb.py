import os
import sys

# paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src/classes")))


from config import TEST_ACCT_KEY
from firefly_client import FireflyClient
from constants import Networks

def main():

  # initialise client
  client = FireflyClient(
        True, # agree to terms and conditions
        Networks["TESTNET_ARBITRUM"], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

  print('Margin bank balance:', client.get_margin_bank_balance());

  # assuming you have usdc ( can check usdc balance using client.get_usdc_balance())
  print('USDC balance:', client.get_usdc_balance());

  # deposit usdc to margin bank
  print('USDC deposited:',client.deposit_usdc_to_bank(10));

  # check margin bank balance
  print('Margin bank balance:', client.get_margin_bank_balance());

if __name__ == "__main__":
    main()