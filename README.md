# JobMatcher

JobMatcher finds job offers in Morocco (ANAPEC, Jobzyn, LinkedIn), ranks them against your CV, and writes a tailored CV, cover letter and email for the ones you pick.

This repository holds the whole project:

```
job_finder/
├── etl/                  Scraping pipeline (Python package)
│   ├── scrapers/         Download offers from ANAPEC, Jobzyn and LinkedIn
│   ├── parsers/          Turn the downloaded HTML into structured offers
│   ├── normalizer.py     Clean and merge the parsed offers
│   ├── load/             Load the offers into Postgres (Supabase)
│   └── core/             HTTP client, database connection, helpers
├── airflow/              Airflow home: the DAG that runs the pipeline
│   ├── dags/job_pipeline.py
│   └── airflow_local_settings.py
├── frontend/             Web app (React, Vite, Supabase)
├── design/               Approved designs: HTML previews of every page (open design/previews/index.html)
├── requirements.txt      Python dependencies for the pipeline
└── setup.py              Installs the etl package
```

Scraped files are written to `data/` when the pipeline runs. That folder is not tracked.

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env` with your Supabase project:

```
VITE_SUPABASE_URL=...
VITE_SUPABASE_PUBLISHABLE_KEY=...
```

---

## Pipeline (Airflow 2.7.2, Python 3.11)

### 1. Install Python 3.11 (Ubuntu / WSL)

```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

### 2. Create a virtual environment and install

```bash
git clone https://github.com/cad0m/job_finder.git
cd job_finder
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
pip install "apache-airflow==2.7.2" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.7.2/constraints-3.11.txt
```

### 3. Point Airflow at the `airflow/` folder

Run this from the project root, in every terminal you use for Airflow:

```bash
export AIRFLOW_HOME="$(pwd)/airflow"
```

### 4. Initialise Airflow

```bash
airflow db init
airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com
```

`airflow db init` creates `airflow.cfg`, the database and the logs inside `airflow/`. They are not tracked. In `airflow.cfg`, set `load_examples = False`.

### 5. Create `.env` in the project root

```
PROXY_USER=xxxx
PROXY_PASS=xxxx
PROXY_HOST=xxxx
PROXY_PORT=xxxx

DB_USER=postgres
DB_PASS=xxxx
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobs
```

### 6. Run Airflow on port 8081

```bash
airflow scheduler &
airflow webserver --port 8081 &
```

Open http://localhost:8081. The `job_pipeline` DAG appears automatically. Trigger it from the UI, or:

```bash
airflow dags trigger job_pipeline
```
