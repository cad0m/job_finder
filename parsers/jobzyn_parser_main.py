from core.utils import FileLoader, Filesaver
from parsers.jobzyn_parser import JobzynParser
import json
import argparse
from rich import print


def parse_all_jobs(input_folder: str = None, output_folder: str = None):
    input_path = input_folder or "data/raw"
    output_path = output_folder or "data/parsed"
    
    print(f"Loading JSON files from {input_path}/jobzyn...")
    
    try:
        json_files = FileLoader(input_path, "jobzyn").load()
        print(f"Found {len(json_files)} JSON files to parse")
        
        success_count = 0
        error_count = 0
        total_jobs = 0
        
        for json_file in json_files:
            if not json_file.endswith(".json"):
                continue
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Parse each job in the items array
                    jobs = [JobzynParser(item).parse() for item in data['items']]
                    total_jobs += len(jobs)
                    
                    # Save each job individually
                    for job in jobs:
                        try:
                            filename = f"{job.job_id}.json"
                            json_data = json.dumps(job.model_dump(), ensure_ascii=False, indent=2)
                            Filesaver(output_path, "jobzyn", filename, json_data).save()
                            success_count += 1
                            print(f"✓ Parsed job: {job.job_title} ({job.job_id})")
                        except Exception as e:
                            error_count += 1
                            print(f"✗ Error saving job: {e}")
                
            except Exception as e:
                error_count += 1
                print(f"✗ Error parsing file {json_file}: {e}")
        
        print(f"\n{'='*50}")
        print(f"Parsing completed!")
        print(f"Total jobs found: {total_jobs}")
        print(f"Success: {success_count} | Errors: {error_count}")
        print(f"Parsed files saved to {output_path}/jobzyn/")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Fatal error during parsing: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse Jobzyn job JSON files')
    parser.add_argument('--input-folder', type=str, help='Input folder containing JSON files')
    parser.add_argument('--output-folder', type=str, help='Output folder for parsed JSON files')
    
    args = parser.parse_args()
    
    parse_all_jobs(args.input_folder, args.output_folder)