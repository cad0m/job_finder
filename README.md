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
├── airflow/              Airflow: the DAG and its Dockerfile
│   ├── dags/job_pipeline.py
│   └── airflow_local_settings.py
├── frontend/             Web app (React, Vite, Supabase)
├── docker-compose.yml    Runs Airflow (scheduler, web UI, its database)
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

## Pipeline (Airflow in Docker)

Needs Docker with Compose.

```bash
cp .env.example .env      # fill in your database, and a proxy if you have one
docker compose up -d
```

Open http://localhost:8081 (user `admin`, password `admin`), unpause `job_etl_pipeline` and trigger it. It runs once a day after that.

The DAG scrapes ANAPEC, Jobzyn and LinkedIn, parses and normalizes the offers, then loads them into your database. Scraped files are written to `data/`.

Without a proxy in `.env`, the scrapers connect directly.

### Test one scraper without the full pipeline

```bash
docker compose run --rm --no-deps -e HOME=/home/airflow --entrypoint python airflow-scheduler \
  -c "import asyncio; from etl.scrapers.anapec_scraper import run_scraper; asyncio.run(run_scraper(1, 2))"
```

`run_scraper(1, 2)` scrapes page 1 only: the end page is not included.

### Stop

```bash
docker compose down
```
