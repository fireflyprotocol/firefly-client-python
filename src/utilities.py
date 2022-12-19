from datetime import datetime
from random import randint
from web3 import Web3


def to_big_number(value, num_decimals=18):    
    return int(value* (10**num_decimals))

def big_number_to_base(value, num_decimals=18):
    return int(value) / 10**num_decimals

def strip_hex_prefix(input):
    if input[0:2] == '0x':
        return input[2:]
    else:
        return input

def address_to_bytes32(addr):
    return '0x000000000000000000000000' + strip_hex_prefix(addr)


def hash_string(value: str): 
    return Web3.soliditySha3(["string"], [value] ).hex()

def bn_to_bytes8(value:int):
    return str("0x"+"0"*16+hex(value)[2:]).encode('utf-8')

def default_value(dict, key, default_value):
    if key in dict:
        return dict[key]
    else:
        return default_value 

def default_enum_value(dict, key, default_value):
    if key in dict:
        return dict[key].value
    else:
        return default_value.value


def current_unix_timestamp():
        return int(datetime.now().timestamp())

def random_number(max_range):
    return current_unix_timestamp() + randint(0, max_range) + randint(0, max_range)

def extract_query(value:dict):
    query=""
    for i,j in value.items():
        query+="&{}={}".format(i,j)
    return query[1:]

def extract_enums(params:dict,enums:list):
    for i in enums:
        if i in params.keys():
            if type(params[i]) == list:
                params[i] = [x.value for x in params[i]]
            else:
                params[i] = params[i].value
    return params