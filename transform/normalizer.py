import os
import json
import pandas as pd
from core.utils import FileLoader

def normalize_data():
    # Load the data
    websites = os.listdir('data/parsed')
    files = []
    for website in websites:
        files.extend(FileLoader("data/parsed", website, "*.json").load())

    df = pd.DataFrame()
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            df = pd.concat([df, pd.json_normalize(json.load(f))], ignore_index=True)

    # Drop duplicates based on job_id, keeping the first occurrence
    df = df.drop_duplicates(subset=['job_id'], keep='first')

    # Optionally drop job_description if not needed
    df.drop(columns=['job_description'], inplace=True)
    
    # Drop rows where job_id is null
    df = df.dropna(subset=['job_id'])

    df.to_csv('jobs.csv', index=False)

normalize_data()
