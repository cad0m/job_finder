from core.client import CurlClient
from selectolax.parser import HTMLParser
from core.utils import Filesaver
import os


class LinkedInScraper:
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    BASE_RAW_FOLDER = os.path.join("data/raw", "linkedin")  

    # Create the raw data folder if it doesn't exist
    os.makedirs(BASE_RAW_FOLDER, exist_ok=True)

    def __init__(self, client: CurlClient) -> None:  
        self.client = client
    
    async def scrape_page(self, location: str, geoId: str, start: int):
        params = {
            "keywords": "",
            "location": location,
            "geoId": geoId,
            'trk': 'public_jobs_jobs-search-bar_search-submit',
            "start": str(start)
        }
        response = await self.client.get(self.BASE_URL, params=params)
        return response  
    
    async def extract_links(self, html: str):
        parser = HTMLParser(html)
        return [job.attributes.get('href') for job in parser.css('a.base-card__full-link')]
    
    async def get_job_data(self, link: str):
        response = await self.client.get(link, {})
        return response
    
    async def save_job_data(self, data: str, filename: str):
        test= Filesaver("data/raw", "linkedin", filename, data)
        test.save()

    