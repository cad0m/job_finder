from models.base_job import BaseJob
from typing import List, Dict, Any
import json
import re


class JobzynParser:
    """Parser for Jobzyn API JSON response"""
    
    BASE_URL = "https://www.jobzyn.com/fr/jobs"
    
    def __init__(self, response_text: str):
        self.response_text = response_text
        self.jobs_data = self._extract_json()
    
    def _extract_json(self) -> List[Dict[str, Any]]:
        """Extract JSON from the response text"""
        try:
            # Response format: 0:["$@1",...]  1:{"items":[...]}
            # Extract the JSON part after "1:"
            match = re.search(r'1:(\{.*\})', self.response_text, re.DOTALL)
            if match:
                json_str = match.group(1)
                # Replace date markers like "$D2025-11-11T09:12:13.150Z" with clean dates
                json_str = re.sub(r'\"\$D([^"]+)\"', r'"\1"', json_str)
                data = json.loads(json_str)
                return data.get('items', [])
            return []
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return []
    
    def parse(self) -> List[BaseJob]:
        """Parse all jobs from response"""
        jobs = []
        for item in self.jobs_data:
            try:
                job = self._parse_job(item)
                jobs.append(job)
            except Exception as e:
                print(f"Error parsing job item: {e}")
                continue
        return jobs
    
    def _parse_job(self, item: Dict[str, Any]) -> BaseJob:
        """Parse single job item to BaseJob model"""
        job_data = item.get('job', {})
        company_data = job_data.get('company', {})
        
        # Build job URL
        slug = job_data.get('slug', '')
        job_url = f"{self.BASE_URL}/{slug}" if slug else None
        
        # Build company URL
        company_slug = company_data.get('slug', '')
        company_url = f"https://www.jobzyn.com/fr/company/{company_slug}" if company_slug else None
        
        # Extract location (cities or country)
        cities = job_data.get('city', [])
        country = job_data.get('country')
        location_parts = []
        if cities:
            location_parts.extend(cities)
        if country:
            location_parts.append(country)
        location = ', '.join(location_parts) if location_parts else None
        
        # Map contract type to employment type
        contract_type = job_data.get('contractType', '')
        employment_type_map = {
            'CDI': 'Full-time',
            'CDD': 'Contract',
            'STAGE': 'Internship',
            'ALTERNANCE': 'Apprenticeship',
            'FREELANCE': 'Freelance'
        }
        employment_type = employment_type_map.get(contract_type, contract_type)
        
        # Remote work to seniority/type info
        remote_work = job_data.get('remoteWork', '')
        remote_map = {
            'REMOTE': 'Remote',
            'HYBRID': 'Hybrid',
            'ONSITE': 'On-site'
        }
        work_type = remote_map.get(remote_work, remote_work)
        
        # Experience range as seniority level
        experience_range = job_data.get('requiredYearsOfExperienceRange', '')
        seniority_level = f"{experience_range} - {work_type}" if experience_range else work_type
        
        return BaseJob(
            job_id=str(job_data.get('id', '')),
            job_title=job_data.get('title'),
            company_name=company_data.get('name'),
            company_logo=company_data.get('logoUrl'),
            location=location,
            posted_date=item.get('publishedAt'),
            num_applicants=None,  # Not available in API response
            job_description=None,  # Need to fetch individual job page for this
            seniority_level=seniority_level,
            employment_type=employment_type,
            job_function=', '.join(job_data.get('categories', [])),
            industries=job_data.get('categories', []),
            job_url=job_url,
            company_url=company_url,
            source="Jobzyn"
        )
