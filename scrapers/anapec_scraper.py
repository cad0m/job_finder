from core.client import CurlClient
from selectolax.parser import HTMLParser
from core.utils import Filesaver
import os
import asyncio
import argparse

class AnapecScraper:
    BASE_URL = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche/"
    BASE_RAW_FOLDER = os.path.join("data/raw", "anapec")  

    def __init__(self, client: CurlClient) -> None:  
        self.client = client
        os.makedirs(self.BASE_RAW_FOLDER, exist_ok=True)

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
        filesaver = Filesaver("data/raw", "anapec", filename, data)
        filesaver.save()
    
    async def scrape_all(self, start_page: int = 1, end_page: int = 5):
        """Main scraping logic - scrapes pages and saves raw HTML"""
        print(f"Starting scrape from page {start_page} to {end_page}")
        
        for page in range(start_page, end_page):
            print(f"Scraping page {page}...")
            html = await self.scrape_page(page)
            links = await self.extract_links(html.text)
            
            print(f"Found {len(links)} job links on page {page}")

            for count, link in enumerate(links):
                try:
                    job_data = await self.get_job_data(f"http://www.anapec.org{link}")
                    filename = f"{page}_{count}.html"
                    await self.save_job_data(job_data.text, filename)
                    print(f"Saved job {page}_{count}")
                except Exception as e:
                    print(f"Error scraping job {page}_{count}: {e}")
        
        await self.client.close()
        print(f"Scraping completed! Files saved to {self.BASE_RAW_FOLDER}")


async def run_scraper(start_page: int, end_page: int):
    """Entry point for running the scraper"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }
    
    client = CurlClient(header=headers)
    scraper = AnapecScraper(client)
    await scraper.scrape_all(start_page, end_page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Anapec job listings')
    parser.add_argument('--start-page', type=int, default=1, help='Start page number')
    parser.add_argument('--end-page', type=int, default=5, help='End page number')
    
    args = parser.parse_args()
    
    asyncio.run(run_scraper(args.start_page, args.end_page))