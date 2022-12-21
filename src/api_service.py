import requests
from interfaces import *

class APIService():
    def __init__(self, url):
        self.server_url = url
        self.auth_token = None
        return
    
    def get(self, service_url, query, auth_required=False):
        """
            Makes a GET request and returns the results
            Inputs:
                - service_url(str): the url to make the request to.
                - query(dict): the get query.
                - auth_required(bool): indicates whether authorization is required for the call or not.  
        """
        url = self._create_url(service_url)
        response = None
        if auth_required:
            response = requests.get(url=url, params=query, headers={'Authorization': 'Bearer {}'.format(self.auth_token)})
        else:
            response = requests.get(url, params=query)

        try:
            return response.json()
        except:
            raise Exception("Error while getting {}: {}".format(url, response))
        
    def post(self, service_url, data, auth_required=False):
        """
            Makes a POST request and returns the results
            Inputs:
                - service_url(str): the url to make the request to.
                - data(dict): the data to post with POST request.
                - auth_required(bool): indicates whether authorization is required for the call or not.
        """
        url = self._create_url(service_url)
        response = None
        if auth_required:
            response = requests.post(url=url, data=data, headers={'Authorization': 'Bearer {}'.format(self.auth_token)})

        else:
            response = requests.post(url=url, data=data)

        if "error" in response:
            raise Exception("Error while posting to {}: {}".format(url, response))
        else:
            return response.json()

    def delete(self,service_url, data, auth_required=False):
        """
            Makes a DELETE request and returns the results
            Inputs:
                - service_url(str): the url to make the request to.
                - data(dict): the data to post with POST request.
                - auth_required(bool): indicates whether authorization is required for the call or not.
        """
        url = self._create_url(service_url)
        if auth_required:
            return requests.delete(url=url, data=data, headers={'Authorization': 'Bearer {}'.format(self.auth_token)}).json()
        else:
            return requests.delete(url=url, data=data).json()
 
    '''
        Private methods
    '''
    def _create_url(self, path):
        """
            Appends namespace to server url
        """
        return "{}{}".format(self.server_url, path)
