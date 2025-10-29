# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07SEP2025

    Purpose         : Global variables for environment setup

    Dependencies    :

    Program name    : globals

    Modifications
    -------------
    07SEP2025   RLEWIS  Initial Version 
    27OCT2025   RLEWIS  Updated to work in Windows
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals          import *
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.python import PythonSensor

# Import your existing ETL functions
from etl.exchange_rates.extract import extract
from etl.exchange_rates.transform import transform
from etl.exchange_rates.load import load
from etl.exchange_rates.check_for_new_data import check_for_new_data
from globals import current_db, data_dir

# --- DAG definition ---
default_args = {
    'owner': 'rob',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'exchange_rates_etl',
    default_args=default_args,
    description='Daily ETL for ECB exchange rates',
    schedule_interval='0 14 * * *',  # 14:00 daily
    start_date=datetime(2025, 10, 28),
    catchup=False
)

# --- Sensor to wait until new XML data is available ---
def wait_for_new_data():
    # Return True if new data is available; False if not (Airflow will retry)
    return check_for_new_data(
        url="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml",
        ns={'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'},
        db_config=current_db
    )

wait_sensor = PythonSensor(
    task_id='wait_for_new_data',
    python_callable=wait_for_new_data,
    poke_interval=3600,  # check every hour
    timeout=24*3600,     # fail if not available after 24 hours
    dag=dag
)

# --- Extract task ---
def extract_task():
    return extract("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")

extract_op = PythonOperator(
    task_id='extract_data',
    python_callable=extract_task,
    dag=dag
)

# --- Transform task ---
def transform_task(ti):  # ti = task instance (Airflow passes it)
    raw_path = ti.xcom_pull(task_ids='extract_data')  # get path from extract
    return transform({'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}, raw_path)

transform_op = PythonOperator(
    task_id='transform_data',
    python_callable=transform_task,
    dag=dag
)

# --- Load task ---
def load_task(ti):
    df = ti.xcom_pull(task_ids='transform_data')  # get DataFrame from transform
    load(current_db, df)

load_op = PythonOperator(
    task_id='load_data',
    python_callable=load_task,
    dag=dag
)

# --- Define task order ---
wait_sensor >> extract_op >> transform_op >> load_op
