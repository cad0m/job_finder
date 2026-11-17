FROM apache/airflow:2.7.2-python3.11

# Python dependencies of the etl package, pinned to Airflow's constraints
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.7.2/constraints-3.11.txt

# The project is mounted at /opt/airflow/project (see docker-compose.yml)
ENV PYTHONPATH=/opt/airflow/project
WORKDIR /opt/airflow/project
