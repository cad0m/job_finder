from scrapers.jobzyn_scraper import JobzynScraper
from core.utils import FileLoader, Filesaver
from parsers.jobzyn_parser import JobzynParser
from core.client import CurlClient
import json
import asyncio

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
    #"sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

async def main():
    client = CurlClient(header=headers)
    scraper = JobzynScraper(client)

    for page in range(1, 15):

        full_json = await scraper.scrape_page(page)
        dict_json = await scraper.extract_dic(full_json.text)
        await scraper.save_job_data(dict_json, f"{page}.json")       
    
    try:
        json_to_parse = FileLoader("data/raw", "jobzyn", "*.json").load()
        for json_file in json_to_parse:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                jobs = [JobzynParser(item).parse() for item in data['items']]
                for job in jobs:
                    Filesaver("data/parsed", "jobzyn", f"{job.job_id}.json", json.dumps(job.model_dump(), ensure_ascii=False)).save()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())