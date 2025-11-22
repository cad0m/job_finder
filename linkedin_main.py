import asyncio
from core.client import CurlClient
from core.utils import Filesaver, FileLoader
from scrapers.linkedin_scraper import LinkedInScraper
from parsers.linkedin_parser import LinkedInJobParser
from rich import print
import json

LOCATION = "morocco"
GEO_ID = ""
START = 0                
MAX_CONCURRENT_REQUESTS = 10

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

async def main():
    
    #create the client that will be used to make the requests
    client = CurlClient(header=headers)

    #create a semaphore to limit the number of concurrent requests
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    try:
        scraper = LinkedInScraper(client)


        #count the errors to break the loop
        count_errors = 0
    
        for start in range(0, 2):
            #scrape the page
            html = await scraper.scrape_page(LOCATION, GEO_ID, start*25)

            #check if the request is successful
            if html.status_code != 200:
                count_errors += 1
                continue
            
            #extract the links of jobs
            links = await scraper.extract_links(html.text)
            
            #extracting and saving job data for each link
            for count, link in enumerate(links):
                async with semaphore:        
                    try:
                        job_data = await scraper.get_job_data(link)
                        await scraper.save_job_data(job_data.text, f"{start}_{count}.html")
                    except Exception as e:
                        print(f"Error: {e}")
        
        try:
            html_to_parse = FileLoader("data/raw", "linkedin", "*.html").load()
            for html in html_to_parse:
                with open(html, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    parser = LinkedInJobParser(html_content)
                    job = parser.parse()
                    Filesaver("data/parsed", "linkedin", f"{job.job_id}.json", json.dumps(job.model_dump(), ensure_ascii=False)).save()
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.close()  

if __name__ == "__main__":
    asyncio.run(main())