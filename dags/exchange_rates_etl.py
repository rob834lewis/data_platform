from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2
import os

default_args = {
    "owner": "data_coven",
    "depends_on_past": False,
    "start_date": datetime(2025, 10, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "exchange_rates_etl",
    default_args=default_args,
    description="ETL DAG to fetch exchange rates and load to Postgres",
    schedule_interval="@hourly",
    catchup=False,
)

def extract(**kwargs):
    print("✅ Extracting data from API")
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={os.environ.get('EXCHANGE_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    
    # Store data in XCom so next task can use it
    kwargs["ti"].xcom_push(key="exchange_rates", value=data)

def transform(**kwargs):
    print("✅ Transforming data")
    ti = kwargs["ti"]
    data = ti.xcom_pull(key="exchange_rates", task_ids="extract")
    
    rates = data["rates"]
    df = pd.DataFrame(list(rates.items()), columns=["currency", "rate"])
    df["date"] = data["date"]
    
    # Push transformed data to XCom
    ti.xcom_push(key="transformed_data", value=df.to_dict(orient="records"))

def load(**kwargs):
    print("✅ Loading data into Postgres")
    ti = kwargs["ti"]
    records = ti.xcom_pull(key="transformed_data", task_ids="transform")
    
    conn = psycopg2.connect(
        host="postgres",  # Docker container hostname
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency VARCHAR(10),
            rate FLOAT,
            date DATE
        )
    """)
    
    # Insert records into table
    for r in records:
        cur.execute(
            "INSERT INTO exchange_rates (currency, rate, date) VALUES (%s, %s, %s)",
            (r["currency"], r["rate"], r["date"])
        )
    
    conn.commit()
    cur.close()
    conn.close()

extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
    provide_context=True,
    dag=dag
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    provide_context=True,
    dag=dag
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load,
    provide_context=True,
    dag=dag
)

extract_task >> transform_task >> load_task
