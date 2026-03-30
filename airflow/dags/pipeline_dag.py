from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
import os

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 0
}

def run_ingest():
    subprocess.check_call(["python", "ingest/ingest_billing.py"])

def run_dbt():
    subprocess.check_call(["dbt", "run", "--profiles-dir", "./dbt"])

def run_dbt_tests():
    subprocess.check_call(["dbt", "test", "--profiles-dir", "./dbt"])

with DAG(
    dag_id="billing_pipeline",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    start_date=datetime(2026,1,1),
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="ingest", python_callable=run_ingest)
    t2 = PythonOperator(task_id="dbt_run", python_callable=run_dbt)
    t3 = PythonOperator(task_id="dbt_test", python_callable=run_dbt_tests)

    t1 >> t2 >> t3