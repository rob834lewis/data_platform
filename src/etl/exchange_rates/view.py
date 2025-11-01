import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="airflow",
    user="airflow",
    password="airflow"
)

# Load the table into a DataFrame
df = pd.read_sql("SELECT * FROM exchange_rates;", conn)
print(df.head())

conn.close()