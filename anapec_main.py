import asyncio
from core.client import CurlClient
from core.utils import Filesaver, FileLoader
from scrapers.anapec_scraper import AnapecScraper
from parsers.anapec_parser import AnapecJobParser
from rich import print
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

async def main():
    client = CurlClient(header=headers)
    scraper = AnapecScraper(client)
    
    # for page in range(1, 20):
    #     html = await scraper.scrape_page("1")
    #     links = await scraper.extract_links(html.text)

    #     for count, link in enumerate(links):
    #         try:
    #             job_data = await scraper.get_job_data(f"http://www.anapec.org{link}")
    #             await scraper.save_job_data(job_data.text, f"{page}_{count}.html")
    #         except Exception as e:
    #             print(f"Error: {e}")
    try:
        html_to_parse = FileLoader("data/raw", "anapec", "*.html").load()
        for count, html in enumerate(html_to_parse):
            with open(html, 'r', encoding='utf-8') as f:
                html_content = f.read()
                parser = AnapecJobParser(html_content)
                job = parser.parse()
                Filesaver("data/parsed", "anapec", f"{count}_{job.job_id}.json", json.dumps(job.model_dump(), ensure_ascii=False)).save()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())