from core.client import CurlClient
from parsers.jobzyn_parser import JobzynParser
from core.utils import Filesaver
from models.base_job import BaseJob
import os
import json


class JobzynScraper:
    BASE_URL = "https://www.jobzyn.com/fr/jobs/maroc"
    BASE_RAW_FOLDER = os.path.join("data/raw", "jobzyn")

    os.makedirs(BASE_RAW_FOLDER, exist_ok=True)

    def __init__(self, client: CurlClient) -> None:
        self.client = client
        self.next_action = "8b5180f2634314d3c1ab9bd77a5db9a443e2c689"
    
    async def scrape_page(self, page: int = 1):
        """Scrape jobs from a specific page"""
        payload = json.dumps([{"page": page}])
        
        headers = {
            "accept": "text/x-component",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "text/plain;charset=UTF-8",
            "next-action": self.next_action,
            "origin": "https://www.jobzyn.com",
            "referer": "https://www.jobzyn.com/fr/jobs/maroc",
        }
        
        response = await self.client.post(self.BASE_URL, data=payload, headers=headers)
        return response
    
    def parse_jobs(self, response_text: str) -> list[BaseJob]:
        """Parse jobs from API response"""
        parser = JobzynParser(response_text)
        return parser.parse()
    
    async def save_raw_response(self, data: str, filename: str):
        """Save raw API response"""
        saver = Filesaver("data/raw", "jobzyn", filename, data)
        saver.save()
    
    async def get_job_details(self, job_url: str):
        """Get detailed job page (for description)"""
        response = await self.client.get(job_url, params={})
        return response
