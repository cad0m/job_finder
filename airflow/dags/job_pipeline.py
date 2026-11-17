import os
import sys

# Help imports whether running under Airflow or running the script directly
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # airflow/dags -> project root
os.chdir(PROJECT_ROOT)  # the scrapers read and write data/ relative to the project root
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import asyncio

# --- package imports (the etl package) ---
from etl.scrapers.anapec_scraper import run_scraper as run_anapec_scraper
from etl.parsers.anapec_parser_main import parse_all_jobs as parse_anapec_jobs

from etl.scrapers.jobzyn_scraper import run_scraper as run_jobzyn_scraper
from etl.parsers.jobzyn_parser_main import parse_all_jobs as parse_jobzyn_jobs

from etl.scrapers.linkedin_scraper import run_scraper as run_linkedin_scraper
from etl.parsers.linkedin_parser_main import parse_all_jobs as parse_linkedin_jobs

from etl.normalizer import Transformer
from etl.load import LoadingPipeline


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


# ============================================================================
# TASK FUNCTIONS
# ============================================================================

def scrape_anapec_task():
    """Scrape Anapec jobs"""
    asyncio.run(run_anapec_scraper(start_page=1, end_page=5))


def scrape_jobzyn_task():
    """Scrape Jobzyn jobs"""
    asyncio.run(run_jobzyn_scraper(start_page=1, end_page=15))


def scrape_linkedin_task():
    """Scrape LinkedIn jobs"""
    asyncio.run(run_linkedin_scraper(
        location='morocco',
        geo_id='',
        num_pages=2,
        max_concurrent=10
    ))


def parse_anapec_task():
    """Parse Anapec jobs"""
    parse_anapec_jobs('data/raw', 'data/parsed')


def parse_jobzyn_task():
    """Parse Jobzyn jobs"""
    parse_jobzyn_jobs('data/raw', 'data/parsed')


def parse_linkedin_task():
    """Parse LinkedIn jobs"""
    parse_linkedin_jobs('data/raw', 'data/parsed')


def normalize_data_task():
    """Normalize all parsed data"""
    transformer = Transformer("data/parsed")
    clean_data = transformer.normalize()
    transformer.save_csv(clean_data)


def load_to_database_task():
    """Load normalized data into database"""
    transformer = Transformer("data/parsed")
    clean_data = transformer.normalize()
    
    pipeline = LoadingPipeline()
    pipeline.run(clean_data)


# ============================================================================
# DAG DEFINITION
# ============================================================================

dag = DAG(
    'job_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline: Scrape → Parse → Normalize → Load',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['etl', 'jobs'],
    max_active_runs=1,
)


# ============================================================================
# CREATE TASKS
# ============================================================================

scrape_anapec = PythonOperator(
    task_id='scrape_anapec',
    python_callable=scrape_anapec_task,
    dag=dag,
)

scrape_jobzyn = PythonOperator(
    task_id='scrape_jobzyn',
    python_callable=scrape_jobzyn_task,
    dag=dag,
)

scrape_linkedin = PythonOperator(
    task_id='scrape_linkedin',
    python_callable=scrape_linkedin_task,
    dag=dag,
)

parse_anapec = PythonOperator(
    task_id='parse_anapec',
    python_callable=parse_anapec_task,
    dag=dag,
)

parse_jobzyn = PythonOperator(
    task_id='parse_jobzyn',
    python_callable=parse_jobzyn_task,
    dag=dag,
)

parse_linkedin = PythonOperator(
    task_id='parse_linkedin',
    python_callable=parse_linkedin_task,
    dag=dag,
)

normalize_data = PythonOperator(
    task_id='normalize_data',
    python_callable=normalize_data_task,
    dag=dag,
)

load_to_database = PythonOperator(
    task_id='load_to_database',
    python_callable=load_to_database_task,
    dag=dag,
)


# ============================================================================
# PIPELINE FLOW
# ============================================================================

# Sequential scraping (proxy limitation)
scrape_anapec >> scrape_jobzyn >> scrape_linkedin

# Parallel parsing (all at once)
scrape_linkedin >> [parse_anapec, parse_jobzyn, parse_linkedin]

# Normalize after all parsing is done
[parse_anapec, parse_jobzyn, parse_linkedin] >> normalize_data

# Load to database
normalize_data >> load_to_database