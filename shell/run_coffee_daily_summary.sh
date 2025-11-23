#!/bin/bash

# Go to the project root
cd /srv/data-coven || exit 1

# Activate virtual environment
source venv/bin/activate

# Run the ETL pipeline
python -m src.apps.coffee_order.scripts.coffee_daily_summary