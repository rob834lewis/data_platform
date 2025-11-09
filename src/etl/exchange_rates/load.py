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

