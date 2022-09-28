import os
import sys
from interfaces import Order
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(directory, "../")))

from web3 import Web3
import utils
import constants


class OrderSigner:
    def __init__(self, network_id, orders_contract_address):
        self.network_id = network_id
        self.contract_address = orders_contract_address

    def get_order_flags(self, order):
        flag = 0 

        if order["reduceOnly"]:
            flag += constants.ORDER_FLAGS["IS_DECREASE_ONLY"] 

        if order["isBuy"]:
            flag += constants.ORDER_FLAGS["IS_BUY"] 
        
        saltBytes = utils.bn_to_bytes32(order["salt"])

        return b''.join([
            "0x".encode('utf-8'), 
            saltBytes[-63:],
            str(flag).encode('utf-8')
            ]).decode()


    def get_domain_hash(self):
        return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
            'bytes32'
        ],
        [
            utils.hash_string(constants.EIP712_DOMAIN_STRING),
            utils.hash_string(constants.EIP712_DOMAIN_NAME),
            utils.hash_string(constants.EIP712_DOMAIN_VERSION),
            self.network_id,
            utils.address_to_bytes32(self.contract_address)
        ]
    ).hex()

        
    def get_order_hash(self, order:Order):
        struct_hash = Web3.solidityKeccak(
            abi_types=[
                'bytes32',
                'bytes32',
                'uint256',
                'uint256',
                'uint256',
                'uint256',
                'bytes32',
                'bytes32',
                'uint256'
                ],
            values=[
                utils.hash_string(constants.EIP712_ORDER_STRUCT_STRING),
                self.get_order_flags(order),
                int(order["quantity"]),
                int(order["price"]),
                int(order["triggerPrice"]),
                int(order["leverage"]),
                utils.address_to_bytes32(order["maker"]),
                utils.address_to_bytes32(order["taker"]),
                int(order["expiration"])
            ]
        )

        return utils.get_eip712_hash(self.get_domain_hash(), struct_hash) if struct_hash else ""
    

    def sign_order(self, order:Order, private_key):
        """
        Used to create an order signature. The method will use the provided key 
        in params(if any) to sign the order.

        Args:
            order (Order): an order containing order fields (look at Order interface)
            private_key (str): private key of the account to be used for signing
 
        Returns:
            string: generated signature
        """
        order_hash = self.get_order_hash(order)
        return utils.sign_hash(order_hash, private_key)




    