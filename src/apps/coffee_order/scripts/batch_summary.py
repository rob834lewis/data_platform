import sqlite3
import pandas as pd
from datetime import datetime

# Connect to database
conn = sqlite3.connect('/srv/data-coven/src/apps/coffee_order/scripts/coffee_orders.db')

# Load orders table
df = pd.read_sql_query("SELECT * FROM orders", conn)

# Aggregate data: total orders per coffee type
summary = df.groupby('coffee_name').agg(
    total_orders=('id', 'count'),
    total_revenue=('coffee_price', 'sum')
).reset_index()

# Add timestamp
summary['summary_date'] = datetime.now()

# Save to a new table
summary.to_sql('daily_summary', conn, if_exists='append', index=False)

print("Batch summary completed:")
print(summary)



#df = pd.read_sql_query("SELECT * FROM daily_summary", conn)