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
    cube = root.find(".//ns:Cube[@time]", ns)
    xml_date = cube.attrib.get("time")
    
    conn = None
    try:
        # 3. Connect to Postgres
        conn = psycopg2.connect(
            host=db_config["host"],
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"]
        )

        # 4. Check if table exists
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'exchange_rates'
                );
            """)
            table_exists = cur.fetchone()[0]

        if not table_exists:
            print("Table 'exchange_rates' does not exist — treating as no data yet.")
            return True  # table missing → definitely new data to load

        # 5. Query latest date
        query = "SELECT MAX(date) FROM exchange_rates;"
        df = pd.read_sql(query, conn)
        latest_date_in_db = df.iloc[0, 0] if not df.empty else None

        if latest_date_in_db is None:
            # Table exists but empty
            return True

        # 6. Compare XML date vs DB date
        return xml_date > latest_date_in_db.isoformat()

    except psycopg2.Error as e:
        print("Database error:", e)
        return True  # safer default → treat as needing to load new data

    finally:
        if conn:
            conn.close()

    
    # ---------------