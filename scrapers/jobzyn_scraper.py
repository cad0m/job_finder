from core.client import CurlClient
from selectolax.parser import HTMLParser
from core.utils import Filesaver
import json
import os
import asyncio
import re



class JobzynScraper:
    BASE_URL = "https://www.jobzyn.com/fr/jobs/maroc"
    BASE_RAW_FOLDER = os.path.join("data/raw", "jobzyn") 


    # Create the raw data folder if it doesn't exist
    os.makedirs(BASE_RAW_FOLDER, exist_ok=True)

    def __init__(self, client: CurlClient) -> None:  
        self.client = client

    async def scrape_page(self, page: int):
        
        page_word = '[{"page":' + str(page) + '}]'
        attrib = {
            "data" : page_word
        }
        response = await self.client.get(self.BASE_URL, params={}, more_attributes=attrib, type="post")
        return response  
    
    async def extract_dic(self, full_json: str):
        dict_json = full_json.split("1:", 1)[1]
        return dict_json
        

    async def save_job_data(self, data: str, filename: str):
        test= Filesaver("data/raw", "jobzyn", filename, data)
        test.save()