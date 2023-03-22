from datetime import datetime
from random import randint
from web3 import Web3
import time

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

def config_logging(logging, logging_level, log_file: str = None):
    """Configures logging to provide a more detailed log format, which includes date time in UTC
    Example: 2021-11-02 19:42:04.849 UTC <logging_level> <log_name>: <log_message>
    Args:
        logging: python logging
        logging_level (int/str): For logging to include all messages with log levels >= logging_level. Ex: 10 or "DEBUG"
                                 logging level should be based on https://docs.python.org/3/library/logging.html#logging-levels
    Keyword Args:
        log_file (str, optional): The filename to pass the logging to a file, instead of using console. Default filemode: "a"
    """

    logging.Formatter.converter = time.gmtime  # date time in GMT/UTC
    logging.basicConfig(
        level=logging_level,
        filename=log_file,
        format="%(asctime)s.%(msecs)03d UTC %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )