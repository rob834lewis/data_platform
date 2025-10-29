# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Transform step for Exchange Rates 

    Dependencies    :

    Program name    : transform

    Modifications
    -------------
    27OCT2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals          import *
from common.functions import get_logger

# ----------------
# --- Logging ---
# ----------------

logger = get_logger("exchange_rates_load")

# ----------------
# --- Function ---
# ----------------

def load(db_config: dict, df: pd.DataFrame):

    """
    Load the transformed DataFrame into PostgreSQL.
    For local testing, it connects to a Docker Postgres instance.
    """
    # --- DB connection ---
    conn = psycopg2.connect(
        host     = db_config["host"]   ,
        dbname   = db_config["dbname"] ,
        user     = db_config["user"]   ,
        password = db_config["password"]
    )
    cur = conn.cursor()

    # --- Create table if it doesn't exist ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            date DATE,
            currency VARCHAR(10),
            rate FLOAT,
            PRIMARY KEY (date, currency)
        )
    """)
    conn.commit()
    logger.info("Table exchange_rates ensured in Postgres.")

    # --- Insert rows ---
    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO exchange_rates (date, currency, rate)
            VALUES (%s, %s, %s)
            ON CONFLICT (date, currency)
            DO UPDATE SET rate = EXCLUDED.rate
            """,
            (row['date'], row['currency'], row['rate'])
        )

    conn.commit()
    logger.info(f"{len(df)} rows inserted into exchange_rates.")

    # --- Close connection ---
    cur.close()
    conn.close()
    logger.info("Postgres connection closed.")
