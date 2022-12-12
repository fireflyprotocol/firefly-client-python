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
        """
            Generates and returns a web3 account object.
            Inputs:
                - private_key(str): The user private key.
        """
        try:
            return self.w3.eth.account.privateKeyToAccount(private_key)
        except Exception as e:
            raise(Exception("Failed to get account, Exception: {}".format(e)))


    def connect(self):
        """
            Creates a connection to Web3 RPC given the RPC url.
        """
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.url))
        except:
            raise(Exception("Failed to connect to Host: {}".format(self.url)))
        return 
    
    def add_contract(self,name,address,market=None):
        """
            Adds contracts to the instance's contracts dictionary. 
            The contract name should match the contract's abi name in ./abi directory or a new abi should be added with the desired name.
            Inputs:
                - name(str): The contract name.
                - address(str): The contract address.
                - market(str): The market this contract belongs to (required for market specific contracts).
        """
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
        """
            Creates and sets the instance's user account
            Inputs:
                - private_key(str): The user's private key.
        """
        self.account = self._create_account(private_key)
        return


    ## GETTERS
    def get_contract(self,name,market=""):
        """
            Returns the contract object.
            Inputs:
                - name(str): The contract name.
                - market(str): The market the contract belongs to (required for market specific contracts).
        """
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
        """
            Returns the contract address. If neither of the inputs provided, will return a dict with all contract addresses.  
            Inputs:
                - name(str): The contract name.
                - market(str): The market the contract belongs to (if only market provided will return all address of market as dict).
        """
        try:
            if market and name:
                return self.contracts[market][name].address
            elif market:
                resp = {}
                for i,j in self.contracts[market].items():
                    resp[i] = j.address
                return resp
            else:
                resp = {}
                for i,j in self.contracts[market].items():
                    if type(j)==dict:
                        for k,l in j.items():
                            resp[i][k] = l.address
                    else:
                        resp[i] = j.address
                return resp
        except Exception as e:
            raise(Exception("Failed to get contract address, Exception: {}".format(e)))

    def get_account(self):
        """
            Returns the user account object. 
        """
        return self.account

    def get_ffly_balance(self):
        """
            Returns user's FFLY token balance.
        """
        try:
            return self.w3.eth.get_balance(self.w3.toChecksumAddress(self.account.address))/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_usdc_balance(self):
        """
            Returns user's USDC token balance on Firefly.
        """
        try:
            contract = self.get_contract(name="USDC")
            return contract.functions.balanceOf(self.account.address).call()/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    def get_margin_bank_balance(self):
        """
            Returns user's Margin Bank balance.
        """
        try:
            contract = self.get_contract(name="MarginBank")
            return contract.functions.getAccountBankBalance(self.account.address).call()/1e18
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))
