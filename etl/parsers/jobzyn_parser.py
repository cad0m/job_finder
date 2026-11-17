from typing import Optional
from etl.core.base import BaseJob
import re


class JobzynParser:
    
    
    def __init__(self, job_item: dict):
        self.item = job_item
        self.job = job_item.get('job', {})
        self.company = self.job.get('company', {})
        
    def parse(self) -> BaseJob:
        job_data = {
            'job_id': self._get_job_id(),
            'job_title': self._get_job_title(),
            'company_name': self._get_company_name(),
            'company_logo': self._get_company_logo(),
            'location': self._get_location(),
            'posted_date': self._get_posted_date(),
            'num_applicants': None,
            'job_description': None,
            'seniority_level': self._get_seniority_level(),
            'employment_type': self._get_employment_type(),
            'job_function': self._get_job_function(),
            'industries': self._get_industries(),
            'salary': self._get_salary(),
            'job_url': self._get_job_url(),
            'company_url': self._get_company_url(),
            'source': 'jobzyn',
        }
        
        return BaseJob(**job_data)
    
    def _get_job_id(self) -> Optional[str]:
        job_id = self.item.get('jobId')
        return str(job_id) if job_id else None
    
    def _get_job_title(self) -> Optional[str]:
        return self.job.get('title')
    
    def _get_company_name(self) -> Optional[str]:
        return self.company.get('name')
    
    def _get_company_logo(self) -> Optional[str]:
        return self.company.get('logoUrl')
    
    def _get_location(self) -> Optional[str]:
        cities = self.job.get('city', [])
        country = self.job.get('country')
        
        if not cities:
            return None
        
        location = ', '.join(cities)
        if country:
            location = f"{location}, {country}"
        
        return location
    
    def _get_posted_date(self) -> Optional[str]:
        date = self.item.get('publishedAt')
        if date and date.startswith('$D'):
            return date[2:]
        return date
    
    def _get_seniority_level(self) -> Optional[str]:
        seniority = self.job.get('requiredYearsOfExperienceRange')
        if not seniority:
            return None
        
        # Remove "ans" from the seniority level
        cleaned = seniority.replace('ans', '').strip()
        
        # Handle "X et plus" format -> convert to "X+"
        if 'et plus' in cleaned.lower():
            # Extract the number before "et plus"
            match = re.search(r'(\d+)\s*et\s*plus', cleaned, re.IGNORECASE)
            if match:
                number = match.group(1)
                return f"{number}+"
        
        return cleaned
    
    def _get_employment_type(self) -> Optional[str]:
        return self.job.get('contractType')
    
    def _get_job_function(self) -> Optional[str]:
        categories = self.job.get('categories', [])
        return ', '.join(categories) if categories else None
    
    def _get_industries(self) -> Optional[list[str]]:
        return self.job.get('categories')
    
    def _get_job_url(self) -> Optional[str]:
        slug = self.job.get('slug')
        return f"https://jobzyn.com/jobs/{slug}" if slug else None
    
    def _get_company_url(self) -> Optional[str]:
        slug = self.company.get('slug')
        return f"https://jobzyn.com/companies/{slug}" if slug else None
    
    def _get_salary(self) -> Optional[str]:
        min_salary = self.job.get('minNetMonthlySalary')
        max_salary = self.job.get('maxNetMonthlySalary')
    
        if min_salary and max_salary:
            return f"{min_salary:,} - {max_salary:,}"
        if min_salary:
            return f"{min_salary:,}"
        if max_salary:
            return f"{max_salary:,}"
        return None

        