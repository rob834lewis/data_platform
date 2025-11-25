# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 25NOV2025

    Purpose         : Query the Exchange Rates data for further manipulation

    Dependencies    :

    Program name    : exchange_rates_query

    Modifications
    -------------
    25NOV2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals          import *
from src.common.functions import wdays, get_logger
    
    # ---------------

# ---------------
# --- Logging ---
# ---------------

logger = get_logger("exchange_rates_query")
    
    # ---------------

# ----------------------
# --- Date Variables ---
# ----------------------

todays_date = wdays().get("todays_date")
    
    # ---------------

# -----------------------
# --- Other Variables ---
# -----------------------

expected_columns    = ['date', 'currency', 'rate']

expected_currencies = ['USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL',
                       'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR', 'EUR']

# ------------
# --- Main ---
# ------------

if detect_environment() == 'gcp':
        
    logger.info(f"Working in GCP environment")
    
    # -------------------
    # BigQuery options
    # -------------------

    logger.info(f"Loading database options")
    db_config = current_db
    
    # big query variables
    gcp_project  = db_config['gcp_project']
    dataset_name = db_config['gcp_dataset']
    table_name   = "exchange_rates"

    # create a BigQuery client object, connected to the specified GCP project
    client = bigquery.Client(project=gcp_project)  

    # set the table ID
    table_id = f"{client.project}.{dataset_name}.{table_name}"

            # ---------------

    # -------------
    # Table Read
    # -------------

    # Validation check that the data for today has been loaded

    max_retries = 48 # 4 hours
    retry_count = 0

    while True:

        try:

            exchange_rates = client.list_rows(table_id).to_dataframe()
            logger.info(f"Table exchange_rates successfully read")

        except:

            logger.error(f"Table {table_id} does not exist.")
            # send email notifying table does not exist
            break

        # check data for today has been loaded 

        latest_date = exchange_rates['date'].max()

        if latest_date == todays_date:            

            logger.info(f"Data for today has been loaded, proceeding with query code")
            break

        else:

            logger.info(f"Data for today has not yet been loaded, going to sleep for 5 minutes")

        retry_count += 1
        if retry_count >= max_retries:
            logger.warning("Maximum retries reached, now exiting loop.")
            exchange_rates = pd.DataFrame() 
            break

        time.sleep(300)

    # Validation check that exchange rates is not empty

    if exchange_rates.empty :

        logger.info(f"Exchange Rates dataframe is empty, code will now finish")

    else:


        """

Check for missing currencies

Check for schema drift

Check for sudden value anomalies (±10% daily move)

Check for duplicates
        
"""


        exchange_rates['currency'].value_counts(dropna=False)

else:

    logger.info(f"Running in a currently unsupported environment, code will now finish")