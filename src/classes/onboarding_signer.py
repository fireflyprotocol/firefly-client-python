import os
import sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(directory, "../")))

from web3 import Web3
import utils
import constants
from interfaces import *
from signer import Signer

class OnboardingSigner(Signer):
    def __init__(self, network_id, domain="firefly", version="1.0"):
        super().__init__()
        self.network_id = network_id
        self.domain = domain
        self.version = version

    def get_domain_hash(self):
        '''
            implementing abstract method in Signer class
        '''
        return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
        ],
        [
            utils.hash_string(constants.EIP712_DOMAIN_STRING_NO_CONTRACT),
            utils.hash_string(self.domain),
            utils.hash_string(self.version),
            self.network_id,
        ]
    ).hex()

    def get_message_hash(self, msg:OnboardingMessage):
        struct_hash = Web3.solidityKeccak(
            abi_types=[
                'bytes32',
                'bytes32',
                'bytes32',
                ],
            values=[
                utils.hash_string(constants.EIP712_ONBOARDING_ACTION_STRUCT_STRING),
                utils.hash_string(msg["action"]),
                utils.hash_string(msg["onlySignOn"]),
            ]
        )
        return self.get_eip712_hash(self.get_domain_hash(), struct_hash) if struct_hash else "";
    
    def sign_msg(self, msg:OnboardingMessage, private_key):
        msg_hash = self.get_message_hash(msg)
        return self.sign_hash(msg_hash, private_key) 


