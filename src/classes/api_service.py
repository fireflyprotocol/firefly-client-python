import requests
from interfaces import *
from constants import SERVICE_URLS

class APIService():
    def __init__(self, url):
        self.server_url = url.removesuffix('/')
        self.auth_token = None
        return
    
    def get(self, service_url, query, auth_required=False):
        url = self._create_url(service_url)
        if auth_required:
            return requests.post(url=url, params=query, headers={'Authorization': 'Bearer {}'.format(self.auth_token)}).json()
        else:
            return requests.get(url, params=query).json()
        
    def post(self, service_url, data, auth_required=False):
        url = self._create_url(service_url)
        if auth_required:
            return requests.post(url=url, data=data, headers={'Authorization': 'Bearer {}'.format(self.auth_token)}).json()
        else:
            return requests.post(url=url, data=data).json()


    '''
        Private methods
    '''
    def _create_url(self, path):
        return "{}{}".format(self.server_url, path)
