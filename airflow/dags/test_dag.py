from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="test_dag",
    start_date=datetime(2025, 1, 1),
    # ⭐️ CHANGED: Use 'schedule' instead of 'schedule_interval' ⭐️
    schedule=None,
    catchup=False,
    tags=["debug"],
) as dag:
    hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow DAG!'"
    )