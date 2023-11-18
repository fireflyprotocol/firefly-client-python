from enum import Enum

import pytest
from web3 import Web3

from firefly_exchange_client.utilities import (address_to_bytes32,
                                               bn_to_bytes8, config_logging,
                                               current_unix_timestamp,
                                               default_enum_value,
                                               default_value, extract_enums,
                                               extract_query, hash_string,
                                               random_number, strip_hex_prefix)


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("0x123", "123"),
        ("123", "123"),
        ("0xABCD", "ABCD"),
    ],
)
def test_strip_hex_prefix(input_string, expected_output):
    """
    Test case to verify strip_hex_prefix function.
    It checks if the hex prefix '0x' is correctly stripped from the input string.
    """
    assert strip_hex_prefix(input_string) == expected_output


def test_address_to_bytes32():
    """
    Test case to verify address_to_bytes32 function.
    It checks if the address is correctly converted to bytes32 format.
    """
    address = "0x123"
    expected_output = "0x000000000000000000000000123"
    assert address_to_bytes32(address) == expected_output


def test_hash_string():
    """
    Test case to verify hash_string function.
    It checks if the input string is correctly hashed using soliditySha3.
    """
    value = "example"
    expected_output = Web3.soliditySha3(["string"], [value]).hex()
    assert hash_string(value) == expected_output


def test_bn_to_bytes8():
    """
    Test case to verify bn_to_bytes8 function.
    It checks if the input value is correctly converted to bytes8 format.
    """
    value = 123
    expected_output = f"0x{'0'*16}{hex(value)[2:]}".encode("utf-8")
    assert bn_to_bytes8(value) == expected_output


def test_default_value():
    """
    Test case to verify default_value function.
    It checks if the function correctly returns the default value when the key is not present in the dictionary.
    """
    data = {"key1": "value1", "key2": "value2"}
    key = "key3"
    default_val = "default"
    assert default_value(data, key, default_val) == default_val


def test_default_enum_value():
    """
    Test case to verify default_enum_value function.
    It checks if the function correctly returns the default enum value when the key is not present in the dictionary.
    """

    class MyEnum(Enum):
        VALUE1 = 1
        VALUE2 = 2

    data = {"key1": MyEnum.VALUE1, "key2": MyEnum.VALUE2}
    key = "key3"
    default_val = MyEnum.VALUE1
    assert default_enum_value(data, key, default_val) == default_val.value


def test_current_unix_timestamp():
    """
    Test case to verify current_unix_timestamp function.
    It checks if the function returns an integer value representing the current UNIX timestamp.
    """
    timestamp = current_unix_timestamp()
    assert isinstance(timestamp, int)


def test_random_number():
    """
    Test case to verify random_number function.
    It checks if the function returns a random number within the specified range.
    """
    max_range = 100
    number = random_number(max_range)
    assert isinstance(number, int)
    assert number >= current_unix_timestamp()
    assert number <= current_unix_timestamp() + max_range * 2


def test_extract_query():
    """
    Test case to verify extract_query function.
    It checks if the function correctly extracts and formats query parameters from a dictionary.
    """
    value = {"param1": "value1", "param2": "value2"}
    expected_output = "param1=value1&param2=value2"
    assert extract_query(value) == expected_output


def test_extract_enums():
    """
    Test case to verify extract_enums function.
    It checks if the function correctly extracts enum values from a dictionary based on the provided enum list.
    """

    class MyEnum(Enum):
        VALUE1 = 1
        VALUE2 = 2

    params = {
        "param1": MyEnum.VALUE1.value,
        "param2": [MyEnum.VALUE2.value, MyEnum.VALUE1.value],
        "param3": "value3",
    }
    enums = [MyEnum.VALUE1, MyEnum.VALUE2]
    expected_output = {
        "param1": MyEnum.VALUE1.value,
        "param2": [MyEnum.VALUE2.value, MyEnum.VALUE1.value],
        "param3": "value3",
    }
    assert extract_enums(params, enums) == expected_output
