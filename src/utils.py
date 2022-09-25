from datetime import datetime
from random import randint
from web3 import Web3
import eth_account


def to_bn(value):
    return int(value*1e18)

def strip_hex_prefix(input):
    if input[0:2] == '0x':
        return input[2:]
    else:
        return input

def address_to_bytes32(addr):
    return '0x000000000000000000000000' + strip_hex_prefix(addr)


def hash_string(value: str): 
    return Web3.soliditySha3(["string"], [value] ).hex()

def bn_to_bytes32(value:int):
    return str("0x"+"0"*64+hex(value)[2:]).encode('utf-8')

def get_eip712_hash(domain_hash, struct_hash):
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


def sign_hash(hash, private_key):
    result = eth_account.account.Account.sign_message(
        eth_account.messages.encode_defunct(hexstr=hash),
        private_key
    )
    return result['signature'].hex() + '01'

def default_value(dict, key, default_value):
    if key in dict:
        return dict[key]
    else:
        return default_value 

def current_unix_timestamp():
        return int(datetime.now().timestamp())

def random_number(max_range):
    return current_unix_timestamp() + randint(0, max_range) + randint(0, max_range)
