from selectolax.parser import HTMLParser
from core.base import BaseJob
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
        """Extract contract type and salary"""
        contract = self._get_field_value("Type de contrat")
        salary = self._get_field_value("Salaire mensuel")

        if contract and salary:
            return f"{contract} - {salary}"
        return contract or salary

    def _get_seniority_level(self) -> str | None:
        """Extract experience/seniority information from the job details."""
        experience = self._get_field_value("Expérience professionnelle")
        if experience:
            cleaned = experience.strip()
            if cleaned.startswith("(") and cleaned.endswith(")"):
                cleaned = cleaned[1:-1].strip()
            return cleaned
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


