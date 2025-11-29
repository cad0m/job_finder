# Job Finder ETL – Airflow 2.7.2 (Python 3.11)

This project uses Apache Airflow to orchestrate the ETL pipeline for Job Finder.  
Follow these steps to install Python 3.11, set up Airflow 2.7.2, configure environment variables, and run the DAG on port **8081**.

---

## 1. Install Python 3.11 (WSL / Ubuntu)

```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```
## 2. Clone the Project

```bash
git clone https://github.com/.../job_finder.git
cd job_finder
```
## 3. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

## 4. Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
## 5. Install Apache Airflow 2.7.2

Airflow requires a specific install command:
```bash
pip install "apache-airflow==2.7.2" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.7.2/constraints-3.11.txt
```
## 6. Set AIRFLOW_HOME

Inside the project root (same level as dags/):
```bash
export AIRFLOW_HOME="$(pwd)/airflow_home"
```

Create the folder:
```bash
mkdir -p airflow_home

## 7. Initialize Airflow Database
```bash
airflow db init
```

Create admin user:
```bash
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com
```
## 8. Create .env File

Inside the project root:
`
job_finder/
    .env     ← create here
    dags/
    job_finder/


The .env must contain:

PROXY_USER=xxxx
PROXY_PASS=xxxx
PROXY_HOST=xxxx
PROXY_PORT=xxxx

DB_USER=postgres
DB_PASS=xxxx
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobs

## 9. Airflow Must Load .env

Add this to dags/job_pipeline.py (already done in project):
```bash
from dotenv import load_dotenv
load_dotenv(".env")
```
## 10. Run Airflow on Port 8081

* Start scheduler:
```bash
airflow scheduler &
```

* Start webserver:
```bash
airflow webserver --port 8081 &
```

Open in browser:

http://localhost:8081


Your DAG should appear automatically.

## 11. Trigger the DAG

From the UI → DAGs → job_pipeline → Trigger DAG
OR:
```bash
airflow dags trigger job_pipeline
```