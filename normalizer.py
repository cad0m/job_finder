import os
import json
import re
from pathlib import Path
from typing import Dict, Optional
import pandas as pd
from core.utils import FileLoader


# ==================== Data Cleaning Functions ====================

def normalize_date(value) -> pd.Timestamp:
    if not value or value == "":
        return pd.NaT
    ts = pd.to_datetime(value, errors="coerce", dayfirst=True)
    return pd.NaT if pd.isna(ts) else ts.normalize()


def parse_salary(value) -> Optional[float]:
    if pd.isna(value):
        return None
    try:
        if isinstance(value, str):
            match = re.search(r"[-+]?[0-9][0-9,\.]*", value)
            if match:
                return float(match.group(0).replace(",", ""))
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value) -> Optional[int]:
    if pd.isna(value):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def clean_string(value) -> Optional[str]:
    if pd.isna(value):
        return None
    cleaned = str(value).strip()
    return None if cleaned in ("", "nan", "None") else cleaned


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    required = [
        "job_id", "job_title", "company_name", "company_logo", "company_url",
        "location", "posted_date", "scraped_at", "num_applicants",
        "job_description", "seniority_level", "employment_type",
        "job_function", "industries", "salary", "job_url", "source"
    ]
    for col in required:
        if col not in df.columns:
            df[col] = None
    return df


# ==================== Dimension Extractors ====================

def extract_sources(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["source"]]
        .dropna(subset=["source"])
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"source": "name"})
    )


def extract_companies(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["company_name", "company_logo", "company_url"]]
        .dropna(subset=["company_name"])
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={
            "company_name": "name",
            "company_logo": "logo_url",
            "company_url": "website"
        })
    )


def extract_locations(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["location"]]
        .dropna(subset=["location"])
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"location": "city"})
    )


def extract_functions(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["job_function"]]
        .dropna(subset=["job_function"])
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"job_function": "name"})
    )


def extract_industries(df: pd.DataFrame) -> pd.DataFrame:
    industries = (
        df.explode("industries")["industries"]
        .dropna()
        .astype(str)
        .str.strip()
        .to_frame()
        .rename(columns={"industries": "name"})
    )
    return (
        industries[industries["name"] != ""]
        .drop_duplicates()
        .reset_index(drop=True)
    )


def extract_jobs(df: pd.DataFrame) -> pd.DataFrame:
    jobs = df[[
        "source", "job_id", "company_name", "location", "job_function",
        "job_title", "job_description", "job_url", "posted_date",
        "scraped_at", "salary", "num_applicants", "seniority_level"
    ]].copy()
    
    return jobs.rename(columns={
        "job_id": "external_id",
        "job_title": "title",
        "num_applicants": "num_application"
    })


def extract_job_industries(df: pd.DataFrame) -> pd.DataFrame:
    job_industries = (
        df[["source", "job_id", "industries"]]
        .explode("industries")
        .dropna(subset=["industries"])
    )
    
    job_industries["industries"] = job_industries["industries"].astype(str).str.strip()
    job_industries = job_industries[job_industries["industries"] != ""]
    
    return job_industries.rename(columns={
        "job_id": "external_id",
        "industries": "industry_name"
    })


# ==================== Main Transformer ====================

class Transformer:
    
    def __init__(self, path: str):
        self.path = path
        self.df = self._load_data()
    
    def _load_data(self) -> pd.DataFrame:
        websites = os.listdir(self.path)
        records = []
        
        for website in websites:
            all_files = FileLoader(self.path, website).load()
            json_files = [f for f in all_files if f.endswith('.json')]
            
            for file in json_files:
                with open(file, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    if json_data.get("job_id"):
                        records.append(json_data)
        
        return pd.json_normalize(records) if records else pd.DataFrame()
    
    def normalize(self) -> Dict[str, pd.DataFrame]:
        df = self.df.copy()
        
        if df.empty:
            raise ValueError("No data loaded; data/parsed may be empty.")
        
        df = ensure_columns(df)
        
        # Clean dates
        df["posted_date"] = df["posted_date"].apply(normalize_date)
        df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")
        
        # Clean numeric fields
        df["salary"] = df["salary"].apply(parse_salary)
        df["num_applicants"] = df["num_applicants"].apply(safe_int)
        
        # Clean string fields
        string_cols = [
            "job_id", "job_title", "company_name", "location", 
            "job_function", "source", "job_url", "seniority_level",
            "employment_type", "job_description"
        ]
        for col in string_cols:
            df[col] = df[col].apply(clean_string)
        
        # Extract dimensions
        print("📋 Extracting dimensions...")
        data = {
            "sources": extract_sources(df),
            "companies": extract_companies(df),
            "locations": extract_locations(df),
            "functions": extract_functions(df),
            "industries": extract_industries(df),
            "jobs": extract_jobs(df),
            "job_industries": extract_job_industries(df),
        }
        
        print(f"  ✓ {len(data['sources'])} sources")
        print(f"  ✓ {len(data['companies'])} companies")
        print(f"  ✓ {len(data['locations'])} locations")
        print(f"  ✓ {len(data['functions'])} functions")
        print(f"  ✓ {len(data['industries'])} industries")
        print(f"  ✓ {len(data['jobs'])} jobs")
        print(f"  ✓ {len(data['job_industries'])} job-industry links")
        
        return data
    
    def save_csv(self, data: Dict[str, pd.DataFrame], output_dir: str = "data/transformed") -> None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n💾 Saving CSV files to {output_dir}...")
        
        filename_map = {
            "sources": "job_source",
            "companies": "company",
            "locations": "location",
            "functions": "job_function",
            "industries": "industry",
            "jobs": "jobs",
            "job_industries": "job_industry"
        }
        
        for key, df in data.items():
            csv_name = filename_map.get(key, key)
            file_path = output_path / f"{csv_name}.csv"
            df.to_csv(file_path, index=False)
            print(f"  ✓ {csv_name}.csv ({len(df)} rows)")
        
        print("✅ All CSV files saved!")


def main():
    print("=" * 60)
    print("JOB DATA NORMALIZATION")
    print("=" * 60)
    print()
    
    transformer = Transformer("data/parsed")
    clean_data = transformer.normalize()
    transformer.save_csv(clean_data)
    
    print("\n" + "=" * 60)
    print("✅ NORMALIZATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()