import pandas as pd
from job_finder.load import queries as Q

def safe_value(val):
    return None if pd.isna(val) else val

def safe_int(val):
    if pd.isna(val):
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


class BaseLoader:
    def __init__(self, db):
        self.db = db
    
    def _batch_execute(self, query, data):
        count = 0
        for row in data:
            self.db.execute(query, row)
            count += 1
        self.db.commit()
        return count
    
    def _print(self, name, count, action="Upserted"):
        print(f"     ✓ {action} {count} {name}")


class DimensionLoader(BaseLoader):
    # Generic loader for simple dimension tables
    def load(self, df, query, column_names, table_name):
        print(f"  → {table_name}")
        if df.empty:
            return 0
        
        data = [tuple(row[col] for col in column_names) for _, row in df.iterrows()]
        count = self._batch_execute(query, data)
        self._print(table_name, count)
        return count


class CompanyLoader(BaseLoader):
    def load(self, df):
        print("  → company")
        if df.empty:
            return 0
        
        data = [
            (row["name"], safe_value(row.get("logo_url")), safe_value(row.get("website")))
            for _, row in df.iterrows()
        ]
        count = self._batch_execute(Q.UPSERT_COMPANY, data)
        self._print("companies", count)
        return count


class JobLoader(BaseLoader):
    def load(self, df):
        print("  → jobs")
        if df.empty:
            return 0
        
        data = [self._prepare_params(row) for _, row in df.iterrows()]
        count = self._batch_execute(Q.UPSERT_JOB, data)
        self._print("jobs", count)
        return count
    
    def _prepare_params(self, row):
        return (
            safe_value(row["source"]),
            safe_value(row["external_id"]),
            safe_value(row.get("company_name")),
            safe_value(row.get("location")),
            safe_value(row.get("job_function")),
            safe_value(row["title"]),
            safe_value(row.get("job_description")),
            safe_value(row.get("job_url")),
            safe_value(row.get("posted_date")),
            safe_value(row.get("scraped_at")),
            safe_value(row.get("salary")),
            safe_int(row.get("num_application")),
            safe_value(row.get("seniority_level"))
        )


class JobIndustryLoader(BaseLoader):
    def load(self, df):
        print("  → job_industry")
        if df.empty:
            return 0
        
        # CRITICAL: Filter invalid rows to prevent SQL errors
        df = df[
            df["source"].notna() & 
            df["external_id"].notna() & 
            df["industry_name"].notna()
        ].copy()
        
        if df.empty:
            return 0
        
        data = [
            (row["industry_name"], row["source"], row["external_id"])
            for _, row in df.iterrows()
        ]
        count = self._batch_execute(Q.INSERT_JOB_INDUSTRY, data)
        self._print("job-industry links", count, "Inserted")
        return count