import asyncio
from core.client import CurlClient
from core.utils import Filesaver
from scrapers.jobzyn_scraper import JobzynScraper
from models.base_job import BaseJob
from rich import print
from rich.console import Console
from rich.table import Table
import json

# Configuration
PAGES_TO_SCRAPE = 5
START_PAGE = 1

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.jobzyn.com/fr/jobs/maroc',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}


async def main():
    console = Console()
    client = CurlClient(header=headers)
    
    try:
        scraper = JobzynScraper(client)
        all_jobs = []

        # Scrape multiple pages
        for page in range(START_PAGE, START_PAGE + PAGES_TO_SCRAPE):
            console.print(f"\n[bold cyan]🔎 Fetching Jobzyn page {page}...[/bold cyan]")
            
            try:
                # Get API response
                response = await scraper.scrape_page(page)
                
                # Save raw response
                await scraper.save_raw_response(response, f"page_{page}.json")
                
                # Parse jobs
                jobs = scraper.parse_jobs(response)
                all_jobs.extend(jobs)
                
                console.print(f"[green]✅ Found {len(jobs)} jobs on page {page}[/green]")
                
                # Display preview
                if jobs:
                    table = Table(title=f"Page {page} Preview")
                    table.add_column("Title", style="cyan")
                    table.add_column("Company", style="magenta")
                    table.add_column("Location", style="green")
                    table.add_column("Type", style="yellow")
                    
                    for job in jobs[:3]:  # Show first 3
                        table.add_row(
                            job.job_title or "N/A",
                            job.company_name or "N/A",
                            job.location or "N/A",
                            job.employment_type or "N/A"
                        )
                    
                    console.print(table)
                
                # Delay between pages
                await asyncio.sleep(1)
                
            except Exception as e:
                console.print(f"[red]❌ Error on page {page}: {e}[/red]")
                continue

        # Save all parsed jobs
        console.print(f"\n[bold green]📊 Total jobs scraped: {len(all_jobs)}[/bold green]")
        
        for job in all_jobs:
            try:
                # Save each job as JSON
                filename = f"{job.job_id}.json"
                job_json = json.dumps(job.model_dump(), ensure_ascii=False, indent=2)
                Filesaver("data/parsed", "jobzyn", filename, job_json).save()
            except Exception as e:
                console.print(f"[red]❌ Error saving job {job.job_id}: {e}[/red]")

        # Summary
        console.print("\n[bold cyan]📈 Scraping Summary:[/bold cyan]")
        console.print(f"  • Total jobs: {len(all_jobs)}")
        console.print(f"  • Companies: {len(set(j.company_name for j in all_jobs if j.company_name))}")
        console.print(f"  • Locations: {len(set(j.location for j in all_jobs if j.location))}")
        
        # Top companies
        companies = {}
        for job in all_jobs:
            if job.company_name:
                companies[job.company_name] = companies.get(job.company_name, 0) + 1
        
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
        
        console.print("\n[bold cyan]🏢 Top Companies:[/bold cyan]")
        for company, count in top_companies:
            console.print(f"  • {company}: {count} jobs")

    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")

    finally:
        await client.close()
        console.print("\n[green]✅ Scraping completed![/green]")


if __name__ == "__main__":
    asyncio.run(main())