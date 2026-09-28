from datetime import datetime, timedelta
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
import sys
import os

sys.path.append('/opt/airflow/scripts')
from extract import fetch_crypto_data
# Dictionary of setting for the tasks
default_args = {
    'owner': 'theodoros',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    "coingecko_daily_etl", # Name
    default_args=default_args, # Settings of the pipeline
    description="A modern data stack pipeline for fetching crypto data daily",
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False, # We dont care about the past

) as dag:
    extract_task = PythonOperator(
        task_id='extract_coingecko_api', # Name of the task
        python_callable=fetch_crypto_data, # Function that we are calling
    )

    extract_task