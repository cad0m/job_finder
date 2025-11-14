from selectolax.parser import HTMLParser
from typing import Dict, Optional
from core.base import BaseJob 
import re

class LinkedInJobParser:
    
    def __init__(self, html_content: str):
        self.tree = HTMLParser(html_content)
        
    def parse(self) -> BaseJob:
        job_data = {
            'job_id': self._get_job_id(),
            'job_title': self._get_job_title(),
            'company_name': self._get_company_name(),
            'company_logo': self._get_company_logo(),
            'location': self._get_location(),
            'posted_date': self._get_posted_date(),
            'num_applicants': int(self._get_num_applicants().split()[0]) if self._get_num_applicants() else None,
            'job_description': self._get_job_description(),
            'seniority_level': self._get_criteria('Seniority level'),
            'employment_type': self._get_criteria('Employment type'),
            'job_function': self._get_criteria('Job function'),
            'industries': [self._get_criteria('Industries')] if self._get_criteria('Industries') else None,
            'job_url': self._get_job_url(),
            'company_url': self._get_company_url(),
            'source': 'linkedin',
        }
        
        return BaseJob(**job_data)
    
    def _get_job_title(self) -> Optional[str]:
        """Extract job title"""
        title = self.tree.css_first('h1.top-card-layout__title')
        if title:
            return title.text(strip=True)
        return None
    
    def _get_company_name(self) -> Optional[str]:
        company = self.tree.css_first('a.topcard__org-name-link')
        if company:
            return company.text(strip=True)
        return None
    
    def _get_company_logo(self) -> Optional[str]:
        logo = self.tree.css_first('img.artdeco-entity-image--square-5')
        if logo:
            return logo.attributes.get('data-delayed-url')
        return None
    
    def _get_location(self) -> Optional[str]:
        location = self.tree.css_first('span.topcard__flavor--bullet')
        if location:
            return location.text(strip=True)
        return None
    
    def _get_posted_date(self) -> Optional[str]:
        date = self.tree.css_first('span.posted-time-ago__text')
        if date:
            return date.text(strip=True)
        return None
    
    def _get_num_applicants(self) -> Optional[str]:
        applicants = self.tree.css_first('span.num-applicants__caption')
        if applicants:
            return applicants.text(strip=True)
        return None
    
    def _get_job_description(self) -> Optional[str]:
        desc_div = self.tree.css_first('div.show-more-less-html__markup')
        if desc_div:
            return desc_div.text(strip=True)
        return None
    
    def _get_criteria(self, criteria_name: str) -> Optional[str]:
        criteria_items = self.tree.css('li.description__job-criteria-item')
        
        for item in criteria_items:
            header = item.css_first('h3.description__job-criteria-subheader')
            if header and criteria_name.lower() in header.text(strip=True).lower():
                text = item.css_first('span.description__job-criteria-text')
                if text:
                    return text.text(strip=True)
        return None
    
    def _get_job_url(self) -> Optional[str]:
        canonical = self.tree.css_first('link[rel="canonical"]')
        if canonical:
            return canonical.attributes.get('href')
        return None
    
    def _get_company_url(self) -> Optional[str]:
        company_link = self.tree.css_first('a.topcard__org-name-link')
        if company_link:
            href = company_link.attributes.get('href')
            if href:
                if href.startswith('http'):
                    return href
                else:
                    return f"https://www.linkedin.com{href}"
        return None
    
    def _get_job_id(self) -> Optional[str]:
        job_url = self._get_job_url()
        if job_url:
            # Extract ID from URL pattern
            match = re.search(r'/view/([^/]+)-(\d+)', job_url)
            if match:
                return match.group(2)
        
        job_card = self.tree.css_first('[data-entity-urn*="jobPosting"]')
        if job_card:
            urn = job_card.attributes.get('data-entity-urn', '')
            match = re.search(r'jobPosting:(\d+)', urn)
            if match:
                return match.group(1)
        
        return None