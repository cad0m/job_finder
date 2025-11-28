from core.utils import Filesaver, FileLoader
from parsers.anapec_parser import AnapecJobParser
import json
import argparse
from rich import print

def parse_all_jobs(input_folder: str = None, output_folder: str = None):
    
    input_path = input_folder or "data/raw"
    output_path = output_folder or "data/parsed"
    
    print(f"Loading HTML files from {input_path}/anapec...")
    
    try:
        html_files = FileLoader(input_path, "anapec").load()
        print(f"Found {len(html_files)} HTML files to parse")
        
        success_count = 0
        error_count = 0
        
        for count, html_path in enumerate(html_files):
            if not html_path.endswith(".html"):
                continue
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                parser = AnapecJobParser(html_content)
                job = parser.parse()
                
                # Save parsed job data
                filename = f"{count}_{job.job_id}.json"
                json_data = json.dumps(job.model_dump(), ensure_ascii=False, indent=2)
                Filesaver(output_path, "anapec", filename, json_data).save()
                
                success_count += 1
                print(f"✓ Parsed job {count}: {job.job_title} ({job.job_id})")
                
            except Exception as e:
                error_count += 1 
    
    except Exception as e:
        print(f"Fatal error during parsing: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse Anapec job HTML files to JSON')
    parser.add_argument('--input-folder', type=str, help='Input folder containing HTML files')
    parser.add_argument('--output-folder', type=str, help='Output folder for JSON files')
    
    args = parser.parse_args()
    
    parse_all_jobs(args.input_folder, args.output_folder)