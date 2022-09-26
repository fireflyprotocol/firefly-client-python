import requests
from interfaces import *
from constants import SERVICE_URLS

class APIService():
    def __init__(self, url):
        self.server_url = url.removesuffix('/')
        self.auth_token = None
    
    def set_auth_token(self, token:str):
        self.auth_token = token

    def get(self, service_url, query=""):
        url = self._create_url(service_url)
        print(url,query)
        response = requests.get(url, params=query)
        return response.json()
    
    def post(self, service_url, query):
        url = self._create_url(service_url)
        response = requests.post(url, data = query)
        return response.json()


    '''
        Private methods
    '''
    def _create_url(self, path):
        return "{}{}".format(self.server_url, path)
