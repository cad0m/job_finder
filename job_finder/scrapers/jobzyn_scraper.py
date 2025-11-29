from job_finder.core.client import CurlClient
from selectolax.parser import HTMLParser
from job_finder.core.utils import Filesaver
import json
import os
import asyncio
import argparse


class JobzynScraper:
    BASE_URL = "https://www.jobzyn.com/fr/jobs/maroc"
    BASE_RAW_FOLDER = os.path.join("data/raw", "jobzyn") 

    def __init__(self, client: CurlClient) -> None:  
        self.client = client
        os.makedirs(self.BASE_RAW_FOLDER, exist_ok=True)

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
        filesaver = Filesaver("data/raw", "jobzyn", filename, data)
        filesaver.save()
    
    async def scrape_all(self, start_page: int = 1, end_page: int = 15):
        """Main scraping logic - scrapes pages and saves raw JSON"""
        print(f"Starting Jobzyn scrape from page {start_page} to {end_page}")
        
        for page in range(start_page, end_page):
            try:
                print(f"Scraping page {page}...")
                full_json = await self.scrape_page(page)
                dict_json = await self.extract_dic(full_json.text)
                await self.save_job_data(dict_json, f"{page}.json")
                print(f"✓ Saved page {page}")
            except Exception as e:
                print(f"✗ Error scraping page {page}: {e}")
        
        await self.client.close()
        print(f"Scraping completed! Files saved to {self.BASE_RAW_FOLDER}")


async def run_scraper(start_page: int, end_page: int):
    """Entry point for running the scraper"""
    headers = {
        "accept": "text/x-component",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "text/plain;charset=UTF-8",
        "next-action": "8b5180f2634314d3c1ab9bd77a5db9a443e2c689",
        "origin": "https://www.jobzyn.com",
        "priority": "u=1, i",
        "referer": "https://www.jobzyn.com/fr/jobs/maroc",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-site": "same-origin",
    }
    
    client = CurlClient(header=headers)
    scraper = JobzynScraper(client)
    await scraper.scrape_all(start_page, end_page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Jobzyn job listings')
    parser.add_argument('--start-page', type=int, default=1, help='Start page number')
    parser.add_argument('--end-page', type=int, default=15, help='End page number')
    
    args = parser.parse_args()
    
    asyncio.run(run_scraper(args.start_page, args.end_page))