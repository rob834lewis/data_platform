# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Load step for Exchange Rates 

    Dependencies    :

    Program name    : load

    Modifications
    -------------
    27OCT2025   RLEWIS  Initial Version
    09NOV2025   RLEWIS  Changed to use SQLAlchemy
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals          import *
from src.common.functions import get_logger

# ----------------
# --- Logging ---
# ----------------

logger = get_logger("exchange_rates_load")

# ----------------
# --- Function ---
# ----------------

def load(db_config: dict, df: pd.DataFrame):

    if detect_environment() == 'gcp':
    
        # ---
        # Upload into BigQuery
        # ---
        
        gcp_project  = db_config['gcp_project']
        dataset_name = db_config['gcp_dataset']
        table_name   = "exchange_rates"

        # Create a BigQuery client object, connected to the specified GCP project.
        # This client will be used to interact with BigQuery (create datasets, load tables, run queries, etc.)
        client = bigquery.Client(project=gcp_project)  

        # Construct the full dataset ID using the project ID and the dataset name.
        dataset_id = f"{client.project}.{dataset_name}"

        try:
            dataset = client.get_dataset(dataset_id)  # Try to fetch dataset
            logger.info(f"Dataset {dataset_id} already exists.")

        except:
            # Create a Dataset object in memory. This does NOT create it in BigQuery yet.
            dataset = bigquery.Dataset(dataset_id)

            # Specify the location of the dataset in BigQuery.
            # "EU" ensures that the dataset is stored in European data centers (matches the bucket location).
            dataset.location = "EU"

            # Actually create the dataset in BigQuery.
            # The parameter exists_ok=True means that if the dataset already exists, it won't throw an error.
            client.create_dataset(dataset, exists_ok=True)
            
            logger.info(f"Created dataset {dataset_id}")

        # ---
        # Define schema for bigquery
        # ---

        # Ensure DataFrame columns match schema names and types

        table_id = f"{dataset_name}.{table_name}"

        table_schema = [
            {"name": "date"    , "type": "DATE"  , "mode": "NULLABLE"},
            {"name": "currency", "type": "STRING", "mode": "NULLABLE"},
            {"name": "rate"    , "type": "FLOAT" , "mode": "NULLABLE"}
        ]

        pandas_gbq.to_gbq(
            df,
            table_id,
            project_id=gcp_project,
            if_exists="append",
            table_schema=table_schema
        )

    else:

        """
        Load the transformed DataFrame into PostgreSQL.
        For local testing, it connects to a Docker Postgres instance.
        """
        # --- DB connection ---
        db_url = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}?sslmode={db_config['sslmode']}"
        )

        engine = create_engine(db_url)

        # --- Create table if it doesn't exist ---
        metadata = MetaData()
        exchange_rates = Table(
            'exchange_rates',
            metadata,
            Column('date', Date, primary_key=True),
            Column('currency', String(10), primary_key=True),
            Column('rate', Float)
        )

        # --- Create table if it doesn't exist ---
        metadata.create_all(engine)
        logger.info("Table exchange_rates created in Postgres.")

        # --- Insert rows ---
        with engine.begin() as conn:  # context manager handles commit/rollback
            for _, row in df.iterrows():
                stmt = insert(exchange_rates).values(
                    date=row['date'],
                    currency=row['currency'],
                    rate=row['rate']
                ).on_conflict_do_update(
                    index_elements=['date', 'currency'],
                    set_={'rate': row['rate']}
                )
                conn.execute(stmt)
        logger.info(f"{len(df)} rows inserted into exchange_rates.")

