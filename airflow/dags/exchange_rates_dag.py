# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 30OCT2025

    Purpose         : DAG for Exchange Rates

    Dependencies    :

    Program name    : exchange_rates_dag

    Modifications
    -------------
    30OCT2025   RLEWIS  Initial Version 
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, ShortCircuitOperator

import os
import sys

# --- Ensure project root is importable ---
sys.path.append("/opt/airflow")  # inside container
sys.path.append("/opt/airflow/dags")  # just in case

# --- Imports from your repo ---
from src.globals import *
from etl.exchange_rates.check_for_new_data import check_for_new_data
from etl.exchange_rates.extract import extract
from etl.exchange_rates.transform import transform
from etl.exchange_rates.load import load
from common.functions import wdays, get_logger


logger = get_logger("exchange_rates_dag")

def run_exchange_rates_etl():
    ecb_xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    ecb_xml_ns  = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'} 
    
    if check_for_new_data(ecb_xml_url, ecb_xml_ns, current_db):
        raw_path = extract(ecb_xml_url)
        df = transform(ecb_xml_ns, raw_path)
        load(current_db, df)
        logger.info("Exchange rates ETL completed successfully.")
    else:
        logger.info("No new data — skipping ETL.")

with DAG(
    dag_id="exchange_rates_etl",
    description="Daily ECB Exchange Rates ETL pipeline",
    schedule="@daily",
    start_date=datetime(2025, 10, 29),
    catchup=False,
    tags=["ecb", "etl", "exchange_rates"]
) as dag:

    etl_task = PythonOperator(
        task_id="run_exchange_rates_etl",
        python_callable=run_exchange_rates_etl,
    )

    etl_task
