import json
import os,sys
from web3 import Web3

class Contracts:
    def __init__(self,url) -> None:
        self.contracts = {}
        self.url = url
        self.w3 = None
        self.abi_path = os.path.join(os.getcwd(),"src/classes/abi")
        self.account = None
        self.connect()


    def _create_account(self,private_key):
        try:
            return self.w3.eth.account.privateKeyToAccount(private_key)
        except Exception as e:
            raise(Exception("Failed to get account, Exception: {}".format(e)))


    def connect(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.url))
        except:
            raise(Exception("Failed to connect to Host: {}".format(self.url)))
        return 
    
    def add_contract(self,name,address,market=None):
        if name+".json" in os.listdir(self.abi_path):
            abi_fp = os.path.join(self.abi_path,name+".json")
            with open(abi_fp,"r") as f:
                abi = json.loads(f.read())["abi"]
            if market:
                self.contracts[market][name] = self.w3.eth.contract(address=address, abi=abi)
            else:
                self.contracts[name] = self.w3.eth.contract(address=address, abi=abi)
        else:
            return "Unknown contract name"
        return 
    
    def set_account(self,private_key):
        self.account = self._create_account(private_key)
        return
    
    def set_contract_address(self,market,contract_name,address):
        self.contracts_addresses[market][contract_name] = address 
        return 


    ## GETTERS
    def get_contract(self,name,market=""):
        try:
            if name in self.contracts.keys():
                return self.contracts[name]
            if market in self.contracts.keys() and name in self.contracts[market].keys():
                return self.contracts[market][name]
            else:
                return "Contract not found"
        except Exception as e:
            raise(Exception("Failed to get contract, Exception: {}".format(e)))

    def get_contract_address(self,market=None,name=None):
        try:
            if market and name:
                return self.contracts[market][name].address
            elif market:
                return self.contracts[market]
            else:
                return self.contracts
        except Exception as e:
            raise(Exception("Failed to get contract address, Exception: {}".format(e)))

    def get_account(self):
        return self.account

    def get_ffly_balance(self):
        try:
            return self.w3.eth.get_balance(self.w3.toChecksumAddress(self.account.address))/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_usdc_balance(self):
        try:
            contract = self.get_contract(name="USDC")
            return contract.functions.balanceOf(self.account.address).call()/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_margin_bank_balance(self):
        try:
            contract = self.get_contract(name="MarginBank")
            return contract.functions.getAccountBankBalance(self.account.address).call()/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))
