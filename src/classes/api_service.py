import requests
from interfaces import *
from constants import SERVICE_URLS

class APIService():
    def __init__(self, url):
        self.server_url = url.removesuffix('/')
        self.auth_token = None
    
    def set_auth_token(self, token:str):
        self.auth_token = token

    def get_orderbook(self, query:GetOrderbookRequest):
        url = self._create_url(SERVICE_URLS["MARKET"]["ORDER_BOOK"])
        response = requests.get(url, params=query)
        return response.json()

    '''
        Private methods
    '''
    def _create_url(self, path):
        return "{}{}".format(self.server_url, path)
