from web3 import Web3
from eth_account import Account, messages
from Order import Order

class OrderSigner:
    def __init__(self,private_key,url) -> None:
        self.web3 = Web3(url)
        self.account = self.web3.eth.account.privateKeyToAccount(private_key)

    def raw_signature(self,types,values):
        hash = Web3.solidityKeccak(abi_types=types,values=values)
        msg = messages.encode_defunct(hexstr=hash.hex())
        return self.account.sign_message(msg).signature.hex()

    def create_order(order:Order):
        
        return 

    