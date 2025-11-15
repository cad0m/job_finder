import os
from curl_cffi import requests
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

class CurlClient:
    
    def __init__(self, cookies={}, header={}):
        self.cookies = cookies
        self.header = header
        self.proxy = {
            'http': f'http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
            'https': f'http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
        }
        self.session = requests.AsyncSession()  
    
    async def get(self, url: str, params: dict, with_proxy: bool = True, more_attributes = None):

        get_param = {
            'url': url,
            'params': params,
            'headers': self.header,
            'cookies': self.cookies,
            #'impersonate': "chrome110",
            **(more_attributes or {})
        }
        if with_proxy:
            get_param['proxies'] = self.proxy
            
        response = await self.session.get(**get_param)
        print(f"Request status: {response.status_code}")
        return response.text  
    
    async def close(self):
        await self.session.close()  