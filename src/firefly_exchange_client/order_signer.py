from web3 import Web3
from .utilities import bn_to_bytes8, hash_string, address_to_bytes32
from .constants import *
from .signer import Signer
from .interfaces import Order


class OrderSigner(Signer):
    def __init__(self, network_id, orders_contract_address, domain="IsolatedTrader", version="1.0"):
        super().__init__()
        self.network_id = network_id
        self.contract_address = orders_contract_address;
        self.domain = domain
        self.version = version 

    def get_order_flags(self, order):
        flag = 0 

        if order["reduceOnly"]:
            flag += ORDER_FLAGS["IS_DECREASE_ONLY"] 

        if order["isBuy"]:
            flag += ORDER_FLAGS["IS_BUY"] 
        
        saltBytes = bn_to_bytes8(order["salt"])

        return b''.join([
            "0x".encode('utf-8'), 
            saltBytes[-15:],
            str(flag).encode('utf-8')
            ]).decode().ljust(66, '0')
    
    def get_domain_hash(self):
        """
            Returns domain hash
        """
        return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
            'bytes32'
        ],
        [
            hash_string(EIP712_DOMAIN_STRING),
            hash_string(self.domain),
            hash_string(self.version),
            self.network_id,
            address_to_bytes32(self.contract_address)
        ]
    ).hex()

    def get_order_hash(self, order:Order):
        """
            Returns order hash.
            Inputs:
                - order: the order to be signed
            Returns:
                - str: order hash
        """
        flags = self.get_order_flags(order)
        struct_hash = Web3.solidityKeccak(
            abi_types=[
                'bytes32',
                'bytes32',
                'uint256',
                'uint256',
                'uint256',
                'uint256',
                'bytes32',
                'uint256'
                ],

            values=[
                hash_string(EIP712_ORDER_STRUCT_STRING),
                flags,
                int(order["quantity"]),
                int(order["price"]),
                int(order["triggerPrice"]),
                int(order["leverage"]),
                address_to_bytes32(order["maker"]),
                int(order["expiration"])
            ]
        ).hex()

        return self.get_eip712_hash(self.get_domain_hash(), struct_hash) if struct_hash else "";

    def sign_order(self, order:Order, private_key):
        """
            Used to create an order signature. The method will use the provided key 
            in params(if any) to sign the order.

            Args:
                order (Order): an order containing order fields (look at Order interface)
                private_key (str): private key of the account to be used for signing
    
            Returns:
                str: generated signature
        """
        order_hash = self.get_order_hash(order)
        return self.sign_hash(order_hash, private_key, "01")

    def sign_cancellation_hash(self,order_hash:list):
        """
            Used to create a cancel order signature. The method will use the provided key 
            in params(if any) to sign the cancel order.

            Args:
                order_hash(list): a list containing all orders to be cancelled
                private_key (str): private key of the account to be used for signing
            Returns:
                str: generated signature
        """
        struct_hash = Web3.solidityKeccak(
            abi_types=['bytes32','bytes32','bytes32'],
            values=[
                hash_string(EIP712_CANCEL_ORDER_STRUCT_STRING),
                hash_string("Cancel Orders"),
                Web3.solidityKeccak(
                    abi_types=['bytes32' for i in range(len(order_hash))],
                    values=[hash for hash in order_hash]
                ).hex()
            ]
        ).hex()
        return self.get_eip712_hash(self.get_domain_hash(), struct_hash) if struct_hash else ""





    