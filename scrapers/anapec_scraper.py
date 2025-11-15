from core.client import CurlClient
from selectolax.parser import HTMLParser
from core.utils import Filesaver
import os
import asyncio

class AnapecScraper:
    BASE_URL = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche/"
    BASE_RAW_FOLDER = os.path.join("data/raw", "anapec")  

    # Create the raw data folder if it doesn't exist
    os.makedirs(BASE_RAW_FOLDER, exist_ok=True)
    
    def __init__(self, client: CurlClient) -> None:  
        self.client = client

    async def scrape_page(self, page: int):
        url = f"{self.BASE_URL}page:{page}/tout:all"
        response = await self.client.get(url, {}, with_proxy=False)
        return response
    
    async def extract_links(self, html: str):
        parser = HTMLParser(html)
        return [job.attributes.get('href') for job in parser.css('a.nyroModal')]
    
    async def get_job_data(self, link: str):
        response = await self.client.get(link, {}, with_proxy=False)
        return response
    
    async def save_job_data(self, data: str, filename: str):
        test= Filesaver("data/raw", "anapec", filename, data)
        test.save()
    

