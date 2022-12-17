import json, os

class Contracts:
    def __init__(self):
        self.contracts = {}
        self.contract_addresses = {}
        self.abi_path = os.path.join(os.getcwd(),"src/abi")

    def set_contract_addresses(self,contract_address,market=None,name=None):
        if market and name:
            if name:
                self.contract_addresses[market][name] = contract_address
            else:
                self.contract_addresses[market] = contract_address
        elif name:
            self.contract_addresses[name] = contract_address
        else:
            self.contract_addresses = contract_address
        return 
    
    def set_contracts(self,contract,name,market=None):        
        if market:
            if market not in self.contracts:
                self.contracts[market] = {}
            if name:
                self.contracts[market][name] = contract
            else:
                self.contracts[market] = contract

        elif name:
            self.contracts[name] = contract
        else:
            self.contracts = contract
        return 
    

    ## GETTERS
    def get_contract_abi(self,name):
        """
            Returns contract abi.
            Inputs:
                - name(str): The contract name.
        """
        if name+".json" in os.listdir(self.abi_path):
            abi_fp = os.path.join(self.abi_path,name+".json")
            with open(abi_fp,"r") as f:
                abi = json.loads(f.read())["abi"]
            return abi
        else:
            return "Unknown contract name"

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

    def get_contract_address(self,name=None,market=None):
        """
            Returns the contract address. If neither of the inputs provided, will return a dict with all contract addresses.  
            Inputs:
                - name(str): The contract name.
                - market(str): The market the contract belongs to (if only market provided will return all address of market as dict).
        """
        try:
            if market and name:
                return self.contract_addresses[market][name]
            elif market:
                return self.contract_addresses[market]
            elif name:
                return self.contract_addresses["auxiliaryContractsAddresses"][name]
            else:
                return self.contract_addresses
        except Exception as e:
            raise(Exception("Failed to get contract address, Exception: {}".format(e)))

