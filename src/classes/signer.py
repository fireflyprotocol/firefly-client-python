from web3 import Web3
import abc
import eth_account

class Signer:
    def __init__(self):
        pass
        
    @abc.abstractmethod
    def get_domain_hash(self):
        '''Method to compute the domain hash'''
        return

    def get_eip712_hash(self, domain_hash, struct_hash):
        return Web3.solidityKeccak(
        [
            'bytes2',
            'bytes32',
            'bytes32'
        ],
        [
            '0x1901',
            domain_hash,
            struct_hash
        ]
    ).hex()


    def sign_hash(self, hash, private_key):
        result = eth_account.account.Account.sign_message(
            eth_account.messages.encode_defunct(hexstr=hash),
            private_key
        )
        return result['signature'].hex() + '01'
