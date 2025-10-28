# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Extract step for Exchange Rates 

    Dependencies    :

    Program name    : check_for_new_data

    Modifications
    -------------
    27OCT2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals          import *
from common.functions import wdays, get_logger

# ---------------
# --- Logging ---
# ---------------

logger = get_logger("exchange_rates")
    
    # ---------------

# ----------------
# --- Function ---
# ----------------

def check_for_new_data(url: str, ns: dict, db_config: dict) -> bool:

    """
    Peek at the ECB XML file and check if new data is available
    compared to the latest date in Postgres.
    
    Parameters:
        url (str)       : URL to fetch XML from.
        ns (dict)       : XML namespace dictionary.
        db_config (dict): Postgres connection info: host, dbname, user, password.
        
    Returns:
        bool: True if new data is available, False otherwise.
    """

    # 1. Fetch XML 
    resp = requests.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    
    # 2. Extract the date from the XML (e.g., <Cube time="YYYY-MM-DD">)
    cube = root.find('.//Cube/Cube', ns)
    xml_date = cube.get('time')  # string, e.g., "2025-10-27"
    print(xml_date)
    
    # 3. Connect to Postgres and find latest date
    conn = psycopg2.connect(
        host     = db_config["host"]   ,
        dbname   = db_config["dbname"] ,
        user     = db_config["user"]   ,
        password = db_config["password"]
    )
    query = "SELECT MAX(date) FROM exchange_rates;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    latest_date_in_db = df.iloc[0, 0]  # this is a datetime.date object or None
    print(latest_date_in_db)

    if latest_date_in_db is None:
        # Table empty → we definitely want to run
        return True
    
    # Compare dates
    return xml_date > latest_date_in_db.isoformat()

    
    # ---------------