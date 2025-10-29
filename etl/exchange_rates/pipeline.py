# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Run the pipeline for Exchange Rates 

    Dependencies    :

    Program name    : pipeline

    Modifications
    -------------
    27OCT2025   RLEWIS  Initial Version
    28OCT2025   RLEWIS  Added logging and check_for_new_data
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals                               import *
from common.functions                      import get_logger, wdays
from etl.exchange_rates.check_for_new_data import check_for_new_data 
from etl.exchange_rates.extract            import extract
from etl.exchange_rates.transform          import transform
from etl.exchange_rates.load               import load

today = wdays().get("todays_date").strftime("%Y-%m-%d")

logger = get_logger("exchange_rates_pipeline")

def main():

    ecb_xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    ecb_xml_ns  = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'} 

    if check_for_new_data(ecb_xml_url, ecb_xml_ns, current_db):

        try:
            logger.info("=== Starting Exchange Rates ETL ===")

            # Step 1: Extract
            raw_file = extract(ecb_xml_url)
            logger.info(f"Extract step complete. File: {raw_file}")

            # Step 2: Transform
            df = transform(ecb_xml_ns, raw_file)
            logger.info(f"Transform step complete. Rows: {len(df)}")

            # Step 3: Load
            load(current_db, df)
            logger.info("Load step complete. Data inserted into Postgres.")

            logger.info("=== ETL Pipeline completed successfully ===")

        except Exception as e:
            logger.exception(f"ETL Pipeline failed: {e}")
            raise
    else:
        logger.info(f"=== ETL Pipeline already run for {today}")

if __name__ == "__main__":
    
    main()
    