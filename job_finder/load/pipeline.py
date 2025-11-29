import pandas as pd
from job_finder.core.databaseConnection import DatabaseConnection
from . import queries as Q
from job_finder.load.loaders import DimensionLoader, CompanyLoader, JobLoader, JobIndustryLoader


class LoadingPipeline:
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def run(self, data):
        print("=" * 60)
        print("DATABASE LOADING PIPELINE")
        print("=" * 60)
        print()
        
        try:
            self.db.connect()
            
            stats = {}
            stats.update(self._load_dimensions(data))
            stats.update(self._load_facts(data))
            stats.update(self._load_bridges(data))
            
            print("=" * 60)
            print("✅ DATABASE LOADING COMPLETE")
            print("=" * 60)
            
            return stats
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise
        finally:
            self.db.close()
    
    def _load_dimensions(self, data):
        print("📊 STEP 1: Loading dimension tables...")
        
        dim_loader = DimensionLoader(self.db)
        
        stats = {
            "sources": dim_loader.load(
                data.get("sources", pd.DataFrame()), 
                Q.UPSERT_SOURCE, 
                ["name"], 
                "job_source"
            ),
            "companies": CompanyLoader(self.db).load(
                data.get("companies", pd.DataFrame())
            ),
            "locations": dim_loader.load(
                data.get("locations", pd.DataFrame()), 
                Q.UPSERT_LOCATION, 
                ["city"], 
                "location"
            ),
            "functions": dim_loader.load(
                data.get("functions", pd.DataFrame()), 
                Q.UPSERT_FUNCTION, 
                ["name"], 
                "job_function"
            ),
            "industries": dim_loader.load(
                data.get("industries", pd.DataFrame()), 
                Q.UPSERT_INDUSTRY, 
                ["name"], 
                "industry"
            ),
        }
        print()
        return stats
    
    def _load_facts(self, data):
        print("📋 STEP 2: Loading jobs fact table...")
        stats = {
            "jobs": JobLoader(self.db).load(data.get("jobs", pd.DataFrame()))
        }
        print()
        return stats
    
    def _load_bridges(self, data):
        print("🔗 STEP 3: Loading job-industry relationships...")
        stats = {
            "job_industries": JobIndustryLoader(self.db).load(
                data.get("job_industries", pd.DataFrame())
            )
        }
        print()
        return stats


# Airflow-friendly functions
def load_all(data):
    return LoadingPipeline().run(data)


def load_dimensions_only(data):
    db = DatabaseConnection()
    db.connect()
    try:
        dim_loader = DimensionLoader(db)
        return {
            "sources": dim_loader.load(data["sources"], Q.UPSERT_SOURCE, ["name"], "job_source"),
            "companies": CompanyLoader(db).load(data["companies"]),
            "locations": dim_loader.load(data["locations"], Q.UPSERT_LOCATION, ["city"], "location"),
            "functions": dim_loader.load(data["functions"], Q.UPSERT_FUNCTION, ["name"], "job_function"),
            "industries": dim_loader.load(data["industries"], Q.UPSERT_INDUSTRY, ["name"], "industry"),
        }
    finally:
        db.close()


def load_jobs_only(data):
    db = DatabaseConnection()
    db.connect()
    try:
        return JobLoader(db).load(data["jobs"])
    finally:
        db.close()


def load_job_industries_only(data):
    db = DatabaseConnection()
    db.connect()
    try:
        return JobIndustryLoader(db).load(data["job_industries"])
    finally:
        db.close()