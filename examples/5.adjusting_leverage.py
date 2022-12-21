from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS



def main():

    # initialize client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )
    

    print('Leverage on BTC market:', client.get_user_leverage(MARKET_SYMBOLS.BTC))
    # we have a position on BTC so this will perform on-chain leverage update
    # must have native chain tokens to pay for gas fee
    client.adjust_leverage(MARKET_SYMBOLS.BTC, 6);

    print('Leverage on BTC market:', client.get_user_leverage(MARKET_SYMBOLS.BTC))


    print('Leverage on ETH market:', client.get_user_leverage(MARKET_SYMBOLS.ETH))
    # since we don't have a position on-chain, it will perform off-chain leverage adjustment
    client.adjust_leverage(MARKET_SYMBOLS.ETH, 4);

    print('Leverage on ETH market:', client.get_user_leverage(MARKET_SYMBOLS.ETH))



if __name__ == "__main__":
    main()