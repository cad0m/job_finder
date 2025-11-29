from selectolax.parser import HTMLParser
from typing import Dict, Optional
from job_finder.core.base import BaseJob 
from datetime import datetime, timedelta
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
            'seniority_level': self._normalize_seniority_level(self._get_criteria('Niveau hiérarchique')),
            'employment_type': self._normalize_employment_type(self._get_criteria('Type d’emploi')),
            'job_function': self._get_criteria('Fonction'),
            'industries': [industry.strip() for industry in self._get_criteria('Secteurs').split(',')] if self._get_criteria('Secteurs') else None,
            'salary': self._get_salary(),
            'job_url': self._get_job_url(),
            'company_url': self._get_company_url(),
            'source': 'linkedin',
        }
        
        return BaseJob(**job_data)
    
    def _get_job_title(self) -> Optional[str]:
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
            ago = date.text(strip=True)
            if 'day' in ago or 'days' in ago:
                days = int(ago.split()[0])
                return (datetime.now() - timedelta(days=days)).strftime('%d-%m-%Y')
            elif 'week' in ago or 'weeks' in ago:
                weeks = int(ago.split()[0])
                return (datetime.now() - timedelta(weeks=weeks)).strftime('%d-%m-%Y')
            elif 'month' in ago or 'months' in ago:
                months = int(ago.split()[0])
                return (datetime.now() - timedelta(days=months*30)).strftime('%d-%m-%Y')
            else:
                return datetime.now().strftime('%d-%m-%Y')
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
    
    def _normalize_seniority_level(self, seniority_level: Optional[str]) -> Optional[str]:
    
        if not seniority_level:
            return None
        
        seniority_lower = seniority_level.lower().strip()
        
        # Mapping des niveaux hiérarchiques vers des plages numériques
        seniority_mapping = {
            # 0-2 ans: Débutants, Stagiaires
            '0 - 1': [
                'stagiaire', 'alternant', 'intern', 'internship', 
                'entry level', 'débutant', 'junior', 'apprenti',
                'graduate', 'trainee'
            ],
            
            # 3-5 ans: Cadres confirmés
            '2 - 5': [
                'cadre', 'associate', 'confirmé', 'confirmed',
                'mid-level', 'mid level', 'niveau intermédiaire'
            ],
            
            # 5-10 ans: Seniors
            '5 - 10': [
                'premier emploi', 'senior', 'expérimenté', 
                'experienced', 'lead', 'principal'
            ],
            
            # 10+ ans: Direction
            '10+': [
                'directeur', 'director', 'executive', 'manager',
                'cadre supérieur', 'cadre sup', 'head of', 'vp',
                'vice president', 'c-level', 'non pertinent'
            ]
        }
        
        # Chercher une correspondance
        for numeric_range, keywords in seniority_mapping.items():
            for keyword in keywords:
                if keyword in seniority_lower:
                    return numeric_range
        
        # Si aucune correspondance, retourner le niveau original
        return seniority_level


    def _normalize_employment_type(self, employment_type: Optional[str]) -> Optional[str]:
       
        if not employment_type:
            return None
        
        employment_type_lower = employment_type.lower().strip()
        
        # Mapping des types d'emploi LinkedIn vers les catégories standardisées
        employment_mapping = {
            # CDI - Permanent positions
            'temps plein': 'CDI',
            'full-time': 'CDI',
            'full time': 'CDI',
            'plein temps': 'CDI',
            
            
            # CDD - Temporary/Contract positions
            'temps partiel': 'CDD',
            'part-time': 'CDD',
            'part time': 'CDD',
            'partiel': 'CDD',
            'temporaire': 'CDD',
            'temporary': 'CDD',
            'contract': 'CDD',
            'contrat': 'CDD',
            'cdd': 'CDD',
            
            # Stage - Internship/Alternance
            'stage': 'Stage',
            'internship': 'Stage',
            'alternance': 'Stage',
            'stagiaire': 'Stage',
            
            # Freelance - Independent contractor
            'freelance': 'Freelance',
        }
        
        # Chercher une correspondance exacte ou partielle
        for key, value in employment_mapping.items():
            if key in employment_type_lower:
                return value
        
        # Si aucune correspondance, retourner le type original
        return employment_type
    
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
    
    def _get_salary(self) -> Optional[str]:
        salary = self._get_criteria('Salary')
        if salary:
            return salary
        
        pay_range = self._get_criteria('Pay range')
        if pay_range:
            return pay_range
        
        compensation = self._get_criteria('Compensation')
        return compensation

        salary_info = self.tree.css_first('span.main-job-card__salary-info')
        if salary_info:
            return salary_info.text(strip=True)
        
        return None