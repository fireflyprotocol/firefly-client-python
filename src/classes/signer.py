from web3 import Web3
import eth_account

class Signer:
    def __init__(self):
        pass
        

    def get_eip712_hash(self, domain_hash, struct_hash):
        """
            Returns the EIP712 hash.
            Inputs:
                - domain_hash: chain domain hash
                - struct_hash: struct hash of information to be signed
        """
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


    def sign_hash(self, hash, private_key, append=''):
        """
            Signs the hash and returns the signature. 
        """
        result = eth_account.account.Account.sign_message(
            eth_account.messages.encode_defunct(hexstr=hash),
            private_key
        )
        return result['signature'].hex() + append
