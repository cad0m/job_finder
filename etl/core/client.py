import os
from curl_cffi import requests
from typing import Optional, Dict
from dotenv import load_dotenv
from etl.core.utils import Sleeper
load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

class CurlClient:
    
    def __init__(self, cookies={}, header={}):
        self.cookies = cookies
        self.header = header
        # Use the proxy only when one is configured in .env
        self.proxy = {
            'http': f'http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
            'https': f'http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
        } if PROXY_HOST else None
        self.session = requests.AsyncSession()  
        self.sleeper = Sleeper(2) #sleepr for 1-3 second to avoid many requests

    async def get(self, url: str, params: dict, with_proxy: bool = True, more_attributes = None, type = "get"):

        get_param = {
            'url': url,
            'params': params,
            'headers': self.header,
            'cookies': self.cookies,
            #'impersonate': "chrome110",
            **(more_attributes or {})
        }

        #some websites block the request if it's from a proxy
        if with_proxy and self.proxy:
            get_param['proxies'] = self.proxy

        if type == "post":
            response = await self.session.post(**get_param)
        else:
            response = await self.session.get(**get_param)

        #check if the request is successful
        if response.status_code == 200:
            print(f" Got it! Request status code: {response.status_code}")
        elif response.status_code == 429:
            await self.sleeper.sleep()
            print(f"Too many requests! Request status code sleeped for {self.sleeper.seconds} seconds and retrying...")
            return await self.get(url, params, with_proxy, more_attributes, type)
        else:
            print(f"Error: Request status code: {response.status_code}")

        return response
    
    
    async def close(self):
        await self.session.close()  