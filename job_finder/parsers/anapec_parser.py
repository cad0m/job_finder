from selectolax.parser import HTMLParser
from job_finder.core.base import BaseJob
from datetime import datetime
import re

class AnapecJobParser:

    def __init__(self, html_content: str):
        self.tree = HTMLParser(html_content)

    def parse(self) -> BaseJob:
        try:
            job_data = {
                'job_id': self._get_job_id(),
                'job_title': self._get_job_title(),
                'company_name': self._get_company_name(),
                'company_logo': self._get_company_logo(),
                'location': self._get_location(),
                'posted_date': self._get_posted_date(),
                'num_applicants': None,
                'job_description': self._get_job_description(),
                'seniority_level': self._get_seniority_level(),
                'employment_type': self._get_employment_type(),
                'job_function': self._get_job_function(),
                'industries': self._get_industries(),
                'salary': self._get_salary(),
                'job_url': self._get_job_url(),
                'company_url': None,
                'source': 'anapec.org',
            }

            return BaseJob(**job_data)
        except Exception as e:
            print(f"Error parsing job: {e}")
            print(f"Job data collected: {job_data}")
            raise

    def _get_field_value(self, label: str) -> str | None:
        normalized_label = label.replace('\u2019', "'")
        for span in self.tree.css('span.small_puce'):
            text = span.text().replace('\xa0', ' ').replace('\u2019', "'").strip()
            if normalized_label in text:
                parent = span.parent
                if not parent:
                    continue
                spans = parent.css('span')
                if len(spans) > 1:
                    return spans[1].text().strip()
        return None

    def _get_job_id(self) -> str | None:
        info_box = self.tree.css_first('.info_offre')
        if info_box:
            text = info_box.text()
            match = re.search(r"([A-Z]{1,2}\.\d{7,}|[A-Z]{2}\d{7,})", text)
            return match.group(1) if match else None
        return None

    def _get_job_title(self) -> str | None:
        title_elem = self.tree.css_first('.ref_offre2')
        if title_elem:
            raw_text = title_elem.text().strip()
            title = re.sub(r'^\(\d+\)\s*', '', raw_text)
            return title.strip()
        return None

    def _get_company_name(self) -> str | None:
        logo = self.tree.css_first('.logo_emp')
        if logo:
            return logo.attributes.get('title')
        return None

    def _get_company_logo(self) -> str | None:
        logo = self.tree.css_first('.logo_emp')
        if logo and logo.attributes.get('src'):
            src = logo.attributes['src']
            # Make absolute URL if relative
            if src.startswith('/'):
                return f"https://www.anapec.org{src}"
            return src
        return None

    def _get_location(self) -> str | None:
        header = self.tree.css_first('h5.ref_offre3')
        if not header:
            header = self.tree.css_first('.ref_offre3')

        if header:
            for span in header.css('span'):
                text = span.text().replace('\xa0', ' ').strip()
                if 'sur' in text:
                    match = re.search(r'sur\s+([^\n\r]+)', text)
                    return match.group(1).strip() if match else text.strip()
        return None

    def _get_posted_date(self) -> str | None:
        info_box = self.tree.css_first('.info_offre')
        if info_box:
            match = re.search(r'Date\s*:\s*(\d{2}/\d{2}/\d{4})', info_box.text())
            if match:
                try:
                    date_obj = datetime.strptime(match.group(1), '%d/%m/%Y')
                    return date_obj.strftime('%d-%m-%Y')
                except ValueError:
                    return match.group(1)
        return None

    def _get_job_description(self) -> str | None:
        parts = []

        characteristics = self._get_field_value("Caractéristiques du poste")
        if characteristics:
            parts.append(characteristics)

        profile = self._get_field_value("Description du profil")
        if profile:
            parts.append(f"Profil recherché:\n{profile}")

        formation = self._get_field_value("Formation")
        if formation:
            parts.append(f"Formation: {formation}")

        languages = self._get_languages()
        if languages:
            parts.append(f"Langues: {languages}")

        return '\n\n'.join(parts) if parts else None

    def _get_languages(self) -> str | None:
        lang_label = None
        for span in self.tree.css('span.small_puce'):
            text = span.text().replace('\xa0', ' ').strip()
            if 'Langues' in text:
                lang_label = span
                break

        if not lang_label or not lang_label.parent:
            return None

        parent = lang_label.parent
        lang_p = None
        for p in parent.css('p'):
            style = p.attributes.get('style', '') if hasattr(p, 'attributes') else ''
            if 'margin-top: -35px' in style:
                lang_p = p
                break

        if not lang_p:
            return None

        text = lang_p.text().strip()
        langs = [line.strip() for line in text.split('\n') if line.strip()]
        return ', '.join(langs) if langs else None

    def _get_employment_type(self) -> str | None:
        """Extract and clean contract type.
        
        Handles cases like:
        - "Choix Multiple: (5) CDD, (5) CDI – Non Diplômé" -> "CDD, CDI"
        - "CDI – Non Diplômé" -> "CDI"
        - "CDD" -> "CDD"
        - "CI" -> "CDI" (fixes typo)
        """
        employment_type = self._get_field_value("Type de contrat")
        if not employment_type:
            return None
        
        employment_type = employment_type.strip()
        
        # If it contains "Choix Multiple:", extract the contract types
        if "Choix Multiple:" in employment_type:
            matches = re.findall(r'\([^)]+\)\s*([A-Z]+)', employment_type)
            if matches:
                # Replace CI with CDI in matches
                matches = ['CDI' if m == 'CI' else m for m in matches]
                return ', '.join(matches)
        
        # Remove common prefixes
        employment_type = re.sub(r'^Choix Multiple:\s*', '', employment_type, flags=re.IGNORECASE)
        
        # Remove suffixes like "– Non Diplômé" or similar
        employment_type = re.sub(r'\s*–\s*[^,]+', '', employment_type)
        employment_type = re.sub(r'\s*-\s*[^,]+', '', employment_type)
        
        # Clean up extra whitespace
        employment_type = re.sub(r'\s+', ' ', employment_type).strip()
        
        # Replace standalone "CI" with "CDI" (word boundary to avoid replacing CI in other words)
        employment_type = re.sub(r'\bCI\b', 'CDI', employment_type)
        
        return employment_type if employment_type else None
    
    def _get_salary(self) -> str | None:
        """Extract salary information and return just the number formatted with dots"""
        # Try different possible labels for salary
        salary_labels = [
            "Salaire mensuel",
            "Salaire",
            "Rémunération",
            "Salaire proposé"
        ]
        
        for label in salary_labels:
            salary = self._get_field_value(label)
            if salary:
                # Extract numbers from the salary string
                # Handle formats like "2000 DHS", "2000 - 3000 DHS", etc.
                # Remove existing dots and commas to avoid confusion
                cleaned = salary.replace('.', '').replace(',', '')
                numbers = re.findall(r'\d+', cleaned)
                
                if numbers:
                    # Convert to integer and format with dots as thousand separators
                    num = int(numbers[0])
                    # Format with dots: 10000 -> "10.000", 2000 -> "2.000"
                    formatted = f"{num:,}".replace(',', '.')
                    return formatted
        
        return None

    def _get_seniority_level(self) -> str | None:
        """Extract experience/seniority information and convert to numeric range."""
        experience = self._get_field_value("Expérience professionnelle")
        if not experience:
            return None
        
        cleaned = experience.strip().lower()
        if cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = cleaned[1:-1].strip()
        
        def convert_to_years(value: int, unit: str) -> float:
            """Convert months to years, return as float."""
            return value / 12 if "mois" in unit else float(value)
        
        def format_number(num: float) -> str:
            """Format number, removing .0 for whole numbers."""
            return str(int(num)) if num == int(num) else str(round(num, 1))
        
        # Handle "moins de X mois/ans" (less than)
        match = re.search(r'moins de\s+(\d+)\s*(mois|ans?)', cleaned)
        if match:
            value = int(match.group(1))
            upper = convert_to_years(value, match.group(2))
            return f"0 - {format_number(upper)}"
        
        # Handle "plus de X ans" (more than)
        match = re.search(r'plus de\s+(\d+)\s*(mois|ans?)', cleaned)
        if match:
            value = int(match.group(1))
            lower = convert_to_years(value, match.group(2))
            return f"{format_number(lower)}+"
        
        # Handle "X mois - Y an(s)" or "X an(s) - Y an(s)" ranges
        match = re.search(r'(\d+)\s*(mois|ans?)\s*[-–]\s*(\d+)\s*(mois|ans?)', cleaned)
        if match:
            val1, unit1, val2, unit2 = int(match.group(1)), match.group(2), int(match.group(3)), match.group(4)
            lower = convert_to_years(val1, unit1)
            upper = convert_to_years(val2, unit2)
            return f"{format_number(lower)} - {format_number(upper)}"
        
        # Handle single value like "2 ans" or "6 mois"
        match = re.search(r'(\d+)\s*(mois|ans?)', cleaned)
        if match:
            value = int(match.group(1))
            years = convert_to_years(value, match.group(2))
            return format_number(years)
        
        return None


    def _get_job_function(self) -> str | None:
        """Extract job function / position from the job details."""
        return self._get_field_value("Poste")


    def _get_industries(self) -> list[str] | None:
        """Extract sector/industry"""
        sector = self._get_field_value("Secteur d'activité")
        return [sector] if sector else None

    def _get_job_url(self) -> str | None:
        """Build job URL from reference ID"""
        job_id = self._get_job_id()
        if job_id:
            match = re.search(r'(\d{7})$', job_id)
            if match:
                return f"https://www.anapec.org/sigec-app-rv/fr/entreprises/bloc_offre_home/{match.group(1)}"
        return None


