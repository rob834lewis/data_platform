#!/bin/bash

# Go to the project root
cd /srv/data-coven || exit 1

# Activate virtual environment
source venv/bin/activate

# Run the ETL pipeline
python -m src.etl.exchange_rates.pipeline