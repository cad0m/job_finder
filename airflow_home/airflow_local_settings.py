# /home/cad0m/job_finder/airflow_home/airflow_local_settings.py
import os
import sys

# Project root (one level up from airflow_home)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure project root is on sys.path so 'scrapers', 'parsers', etc. are importable
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
