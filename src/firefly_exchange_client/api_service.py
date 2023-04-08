import aiohttp
from .interfaces import *

class APIService():
    def __init__(self, url:str) -> None:
        self.server_url = url
        self.auth_token = None
        self.client = aiohttp.ClientSession() 

    async def close_session(self) -> None:
        if self.client is not None:
            return await self.client.close()

    async def get(self, service_url:str, query:dict={}, auth_required:bool=False) -> dict:
        """
            Makes a GET request and returns the results
            Inputs:
                - service_url: the url to make the request to.
                - query: the get query.
                - auth_required: indicates whether authorization is required for the call or not.  
        """
        url = self._create_url(service_url)

        response = None
        if auth_required:
            response = await self.client.get(
                url, 
                params=query, 
                headers={'Authorization': 'Bearer {}'.format(self.auth_token)})
        else:
            response = await self.client.get(url, params=query)

        try:
            return await response.json()
        except:
            raise Exception("Error while getting {}: {}".format(url, response))
        
    async def post(self, service_url:str, data:dict, auth_required:bool=False) -> dict:
        """
            Makes a POST request and returns the results
            Inputs:
                - service_url: the url to make the request to.
                - data: the data to post with POST request.
                - auth_required: indicates whether authorization is required for the call or not.
        """
        url = self._create_url(service_url)
        response = None

        if auth_required:
            response = await self.client.post(
                url=url, 
                data=data, 
                headers={'Authorization': 'Bearer {}'.format(self.auth_token)})
        else:
            response = await self.client.post(url=url, data=data)

        try:
            return await response.json()
        except:
            raise Exception("Error while posting to {}: {}".format(url, response))
        
    async def delete(self,service_url:str, data:dict, auth_required:bool=False) -> dict:
        """
            Makes a DELETE request and returns the results
            Inputs:
                - service_url: the url to make the request to.
                - data: the data to post with POST request.
                - auth_required: indicates whether authorization is required for the call or not.
        """
        url = self._create_url(service_url)

        response = None
        if auth_required:
            response = await self.client.delete(
                url=url, 
                data=data, 
                headers={'Authorization': 'Bearer {}'.format(self.auth_token)})
        else:
            response = await self.client.delete(url=url, data=data)
        
        try:
            return await response.json()
        except:
            raise Exception("Error while posting to {}: {}".format(url, response))
 
    '''
        Private methods
    '''
    def _create_url(self, path:str) -> str:
        """
            Appends namespace to server url
            Inputs:
                - path: the route name/path
        """
        return "{}{}".format(self.server_url, path)
