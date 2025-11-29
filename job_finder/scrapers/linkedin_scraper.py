from job_finder.core.client import CurlClient
from selectolax.parser import HTMLParser
from job_finder.core.utils import Filesaver
import os
import asyncio
import argparse


class LinkedInScraper:
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    BASE_RAW_FOLDER = os.path.join("data/raw", "linkedin")  

    def __init__(self, client: CurlClient) -> None:  
        self.client = client
        os.makedirs(self.BASE_RAW_FOLDER, exist_ok=True)
    
    async def scrape_page(self, location: str, geoId: str, start: int):
        params = {
            "keywords": "",
            "location": location,
            "geoId": geoId,
            'trk': 'public_jobs_jobs-search-bar_search-submit',
            "start": str(start)
        }
        print(f"Scraping with params: {params}")
        response = await self.client.get(self.BASE_URL, params=params)
        return response  
    
    async def extract_links(self, html: str):
        parser = HTMLParser(html)
        return [job.attributes.get('href') for job in parser.css('a.base-card__full-link')]
    
    async def get_job_data(self, link: str):
        response = await self.client.get(link, {})
        return response
    
    async def save_job_data(self, data: str, filename: str):
        filesaver = Filesaver("data/raw", "linkedin", filename, data)
        filesaver.save()
    
    async def scrape_all(
        self, 
        location: str = "morocco", 
        geo_id: str = "", 
        num_pages: int = 2,
        max_concurrent: int = 10
    ):
        """
        Main scraping logic - scrapes LinkedIn job pages and saves raw HTML
        
        Args:
            location: Location to search (e.g., "morocco")
            geo_id: LinkedIn geo ID for the location
            num_pages: Number of pages to scrape (25 jobs per page)
            max_concurrent: Maximum concurrent requests
        """
        print(f"Starting LinkedIn scrape: {location}, {num_pages} pages, max {max_concurrent} concurrent")
        
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        count_errors = 0
        total_jobs = 0
        
        for page in range(num_pages):
            start = page * 25
            print(f"\nScraping page {page + 1}/{num_pages} (start={start})...")
            
            try:
                # Scrape the page
                html = await self.scrape_page(location, geo_id, start)
                
                # Check if request was successful
                if html.status_code != 200:
                    count_errors += 1
                    print(f"✗ Error: Status code {html.status_code}")
                    continue
                
                # Extract job links
                links = await self.extract_links(html.text)
                print(f"Found {len(links)} job links on page {page + 1}")
                
                # Scrape each job detail page with concurrency control
                tasks = []
                for count, link in enumerate(links):
                    tasks.append(self._scrape_job_with_semaphore(semaphore, link, page, count))
                
                # Wait for all jobs on this page to complete
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Count successes
                successful = sum(1 for r in results if r is True)
                total_jobs += successful
                print(f"Page {page + 1}: {successful}/{len(links)} jobs saved successfully")
                
            except Exception as e:
                print(f"✗ Error on page {page + 1}: {e}")
                count_errors += 1
        
        await self.client.close()
        
        print(f"\n{'='*50}")
        print(f"Scraping completed!")
        print(f"Total jobs saved: {total_jobs}")
        print(f"Page errors: {count_errors}")
        print(f"Files saved to {self.BASE_RAW_FOLDER}")
        print(f"{'='*50}")
    
    async def _scrape_job_with_semaphore(self, semaphore, link, page, count):
        """Helper to scrape a single job with semaphore control"""
        async with semaphore:
            try:
                job_data = await self.get_job_data(link)
                await self.save_job_data(job_data.text, f"{page}_{count}.html")
                print(f"  ✓ Saved job {page}_{count}")
                return True
            except Exception as e:
                print(f"  ✗ Error on job {page}_{count}: {e}")
                return False


async def run_scraper(
    location: str,
    geo_id: str,
    num_pages: int,
    max_concurrent: int
):
    """Entry point for running the scraper"""
    headers = {
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.linkedin.com/jobs/search?keywords=&location=Morocco&geoId=102787409&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }
    
    client = CurlClient(header=headers)
    scraper = LinkedInScraper(client)
    await scraper.scrape_all(location, geo_id, num_pages, max_concurrent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape LinkedIn job listings')
    parser.add_argument('--location', type=str, default='morocco', help='Location to search')
    parser.add_argument('--geo-id', type=str, default='', help='LinkedIn geo ID')
    parser.add_argument('--num-pages', type=int, default=3, help='Number of pages to scrape')
    parser.add_argument('--max-concurrent', type=int, default=10, help='Max concurrent requests')
    
    args = parser.parse_args()
    
    asyncio.run(run_scraper(
        args.location,
        args.geo_id,
        args.num_pages,
        args.max_concurrent
    ))