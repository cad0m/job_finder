import os
import json
import pandas as pd
from core.utils import FileLoader



def normalize_data():
    # Load the data
    websites = os.listdir('data/parsed')
    
    #extract all json paths
    files = []
    for website in websites:
        files.extend(FileLoader("data/parsed", website, "*.json").load())
    
    #creating dataframe
    df = pd.DataFrame()

    #normalize json files into one df
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            df = pd.concat([df, pd.json_normalize(json.load(f))], ignore_index=True)
            
    df.drop(columns=['job_description'], inplace=True)
    df.to_csv('jobs.csv', index=False)

normalize_data()
