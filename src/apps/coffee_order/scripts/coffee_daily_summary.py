# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
Written by      : Rob Lewis

Date            : 22NOV2025

Purpose         : Daily summary from the Coffee Ordering App

Dependencies    :

Program name    : coffee_daily_summary

Modifications
-------------
22NOV2025   RLEWIS  Initial Version
23NOV2025   RLEWIS  Added date clause
24NOV2025   RLEWIS  Set _ for sql output
----------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import sqlite3
import pandas as pd
import logging
from datetime import datetime
import dateutil.parser

        # ---------------

# -----------------
# --- Functions ---
# -----------------

# Pass ddmonyyyy to date
def d(dte):
    return dateutil.parser.parse(dte).date()

        # -----------------

# ---------------
# --- Logging ---
# ---------------

log_file = '/srv/data-coven/src/logs/coffee_daily_summary.log' # file for storing log

logging.basicConfig(
    level    = logging.INFO                               ,
    format   = '%(asctime)s - %(levelname)s - %(message)s',
    filename = log_file                                   ,
    filemode = 'a'
)

# console handler to enable logging to appear in the output window
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

logging.info(f"Starting daily summary process...")

        # -----------------

# ------------
# --- Main ---
# ------------

# Connect to database
logging.info(f"Connecting to database...")
conn = sqlite3.connect('/srv/data-coven/src/apps/coffee_order/scripts/coffee_orders.db')

# Load orders table
df = pd.read_sql_query("SELECT * FROM orders", conn)

# create date column
df['date'] = pd.to_datetime(df['created_at']).astype('date32[pyarrow]')

# keep today's date
df = df[df['date'] == datetime.now().date()]

if df.shape[0] > 0:

    # New Coffee Orders today
    logging.info(f"Summarising today's coffee orders...")

    # Aggregate data: total orders per coffee type
    daily_summary = df.groupby(['date', 'coffee_name']).agg(
        total_orders=('id', 'count'),
        total_revenue=('coffee_price', 'sum')
    ).reset_index()

    # Save to a new table
    _ = daily_summary.to_sql('daily_summary', conn, if_exists='append', index=False)

else:
    # No new Coffee Orders today
    logging.info(f"No new coffee orders today.")
