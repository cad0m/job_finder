# airflow/airflow_local_settings.py
import os
import sys

# Project root (one level up from airflow/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure project root is on sys.path so the etl package is importable
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
