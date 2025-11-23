

import sqlite3
import pandas as pd

conn = sqlite3.connect('/srv/data-coven/src/apps/coffee_order/scripts/coffee_orders.db')

lookup = pd.read_sql_query("SELECT * FROM daily_summary", conn)
lookup