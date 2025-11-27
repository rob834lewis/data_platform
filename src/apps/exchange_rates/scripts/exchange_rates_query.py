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
    26NOV2025   RLEWIS  Added Validation methods and GBP View
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
    
    # ---------------


# -----------------
# --- Functions ---
# -----------------
    
def table_read(env) -> pd.DataFrame | None :

    if env == 'gcp':

        try:

            df = client.list_rows(table_id).to_dataframe()
            logger.info(f"Table exchange_rates successfully read")
            return df

        except Exception as e:

            logger.error(f"Error reading table {table_id}: {e}")
            return None


# stretch -> create a class to hold these validation funcs

def validate_columns(df) -> pd.DataFrame | None :

    # ---
    # Validation check that expected columns are present
    # ---

    missing_cols = set(expected_columns) - set(df.columns)
    extra_cols   = set(df.columns) - set(expected_columns)

    if missing_cols:

        logger.warning(f"Missing required columns: {missing_cols}")
        return None
    
    else:

        if extra_cols:

            logger.warning(f"Unexpected columns present (schema drift): {extra_cols}")

            # keep only the expected columns
            df = df[expected_columns]

        return df


def validate_datatypes(df) -> pd.DataFrame | None :

    # ---
    # Validation check on data types 
    # ---

    parsed_dates  = pd.to_datetime(df['date'], errors='coerce')
    invalid_dates = parsed_dates.isna()

    if invalid_dates.any():

        logger.error(f"Invalid date values found at rows: {invalid_dates[invalid_dates].index.tolist()}")
        return None

    else:

        logger.info("All values in 'date' column are valid dates")
        df['date'] = pd.to_datetime(df['date']).dt.date

        if not pd.api.types.is_numeric_dtype(df['rate']):

            logger.error("Invalid type for column 'rate', it must be numeric")
            return None

        else: 

            df['rate'] = df['rate'].astype('float64[pyarrow]')

            if not pd.api.types.is_string_dtype(df['currency']):

                logger.error("Invalid type for column 'currency', it must be string")
                return None

            else: 

                df['currency'] = df['currency'].astype('string[pyarrow]')    
                return df

def validate_loaded_today(df) -> pd.DataFrame | None :

    # ---
    # Validation check on loaded date
    # ---

    latest_date = df['date'].max()

    if latest_date == todays_date:            

        logger.info(f"Data for today has been loaded, proceeding with query code")
        return df

    else:

        logger.warning(f"Data for today has not yet been loaded")
        return None

def validate_currencies(df) -> pd.DataFrame | None :

    # ---
    # Validation check that all currencies have been populated
    # ---

    # normalise currency field first in case of mixed case
    df['currency'] = df['currency'].str.upper()

    received_currencies = set(df['currency'].unique())
    missing_currencies  = set(expected_currencies) - received_currencies

    if missing_currencies:

        logger.warning(f"Missing expected currencies: {missing_currencies}")
        return None

    else:

        logger.info("All expected currencies received")
        return df

def validate_duplicates(df) -> pd.DataFrame | None :

    # ---
    # Validation check that there are not duplicates
    # ---
    
    dupes = df[df.duplicated(subset=['date', 'currency'], keep=False)]

    if not dupes.empty:

        logger.warning("Duplicate records found:")
        logger.warning(dupes.to_string(index=False))

        # remove duplicates, no current identification for "true" record
        df = df.drop_duplicates(subset=['date', 'currency'], keep = 'last')
        return df

    else:

        logger.info("No duplicates found.")
        return df

def validate_anomalies(df) -> pd.DataFrame | None :

    # ---
    # Validation check for sudden value movements
    # ---
    
    # Sort
    df = df.sort_values(['currency', 'date'])

    # Calculate daily percentage change
    df['pct_change'] = df.groupby('currency')['rate'].pct_change()

    # Flag anomalies

    anomaly_threshold = 0.10

    value_anomalies = df[
        (df['date'] == todays_date) &
        (df['pct_change'].abs() > anomaly_threshold)
    ]

    df = df.drop(columns = ['pct_change'])

    if not value_anomalies.empty:
        logger.warning(f"Detected possible rate anomalies (>{anomaly_threshold}% change):")
        logger.warning(value_anomalies.to_string(index=False))
        return df
        
    else:

        logger.info("No rate anomalies detected.")
        return df

# sleep function
def retry_sleep():
    logger.info("Sleeping for 5 minutes before retry...")
    time.sleep(300)

    # ---------------

# ------------
# --- Main ---
# ------------


# ---
# set environment options
# --

current_environment = detect_environment()

if current_environment == 'gcp':
        
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

else:

    logger.info(f"Running in a currently unsupported environment, code will now finish")

    # this code is currently only setup to work inside of GCP so will exit if in any other environment
    sys.exit(0)

        # ---------------


# ---
# carry out validations
# ---

# validation functions to call
validations = [
    validate_columns,
    validate_datatypes,
    validate_loaded_today,
    validate_currencies,
    validate_duplicates,
    validate_anomalies
]

# run through checks

max_retries = 48 # 4 hours with 5 minute intervals
retry_count = 0

while retry_count < max_retries:

    # First check that the data for today has been loaded
    df = table_read(current_environment)

    if df is None or df.empty:

        retry_count += 1
        
        logger.warning(f"Retry {retry_count}/{max_retries}: There was an issue reading the table, please investigate")

        retry_sleep()
        continue

    # Track validation failures
    failed_validation = None

    # Loop through remaining validations
    for check in validations:

        df_result = check(df)

        if df_result is None:

            failed_validation = check.__name__
            break

        else:

            df = df_result

    if failed_validation:

        retry_count += 1
        
        logger.warning(f"Retry {retry_count}/{max_retries}: Validation '{failed_validation}' failed")

        retry_sleep()        
        continue

    else:

        # All validations passed
        exchange_rates = df
        logger.info("All validations passed. Proceeding with processing")

        break

# After max retries, log and exit or raise alert
if retry_count >= max_retries:

    logger.error(f"Maximum retries reached ({max_retries}). Exiting process")
    exit(0)
    # !!!Add email functionality!!!

        # ---------------


# ---
# GBP view - could be tweaked to pass any currency
# ---

# pivot exchange_rates so each currency is a column
exchange_rates_pivot = exchange_rates.pivot(index = 'date', columns = 'currency', values = 'rate').reset_index()
exchange_rates_pivot = exchange_rates_pivot.sort_values(by = ['date'])

# Normalise to GBP
currency_cols = [c for c in exchange_rates_pivot.columns if c != 'date']

for currency in currency_cols:
    exchange_rates_pivot[currency] = exchange_rates_pivot[currency] / exchange_rates_pivot['GBP']

# round
exchange_rates_pivot = exchange_rates_pivot.round(4)

# melt back for further use in web output for example
exchange_rates_output = exchange_rates_pivot.melt(id_vars='date', var_name='currency', value_name='rate')

# write gbp rate view to db
if current_environment == 'gcp':

    try:

        gbp_rates_view_table = f"{gcp_project}.{dataset_name}.gbp_rates_view"

        table_schema = [
            {"name": "date"    , "type": "DATE"  , "mode": "NULLABLE"},
            {"name": "currency", "type": "STRING", "mode": "NULLABLE"},
            {"name": "rate"    , "type": "FLOAT" , "mode": "NULLABLE"}
        ]

        pandas_gbq.to_gbq(
            exchange_rates_output,
            gbp_rates_view_table,
            project_id=gcp_project,
            if_exists="replace",
            table_schema=table_schema
        )
        
        logger.info(f"Uploaded GBP exchange rate view into {gbp_rates_view_table}")


    except Exception as e:

        logger.error(f"Failed to upload into {gbp_rates_view_table}: {e}")


        # ---------------