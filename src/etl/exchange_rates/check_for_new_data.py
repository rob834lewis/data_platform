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
    02NOV2025   RLEWIS  Changed print to logging
    09NOV2025   RLEWIS  Changed to use SQLAlchemy
    13NOV2025   RLEWIS  Added testing vars
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals          import *
from src.common.functions import get_logger

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

    """

    Testing
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    ns  = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'} 
    db_config = current_db
    
    """

    # 1. Fetch XML 
    resp = requests.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    
    # 2. Extract the date from the XML (e.g., <Cube time="YYYY-MM-DD">)
    cube = root.find(".//ns:Cube[@time]", ns)
    xml_date = cube.attrib.get("time")

    try:
        # 3. Connect to Postgres
        db_url = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}?sslmode={db_config['sslmode']}"
        )

        engine = create_engine(db_url)

        # 4. Check if table exists
        table_check_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'exchange_rates'
        );
        """
        with engine.connect() as conn:
            table_exists = conn.execute(text(table_check_query)).scalar()

        if not table_exists:
            logger.info("Table 'exchange_rates' does not exist — treating as no data yet.")
            return True  # table missing -> definitely new data to load

        # 5. Query latest date
        latest_query = "SELECT MAX(date) FROM exchange_rates;"
        df = pd.read_sql(latest_query, engine)
        latest_date_in_db = df.iloc[0, 0] if not df.empty else None

        if latest_date_in_db is None:
            # Table exists but empty
            return True

        # 6. Compare XML date vs DB date
        return xml_date > latest_date_in_db.isoformat()

    except Exception as e:
        logger.error("Database error:", exc_info=e)
        return True  # safer default -> treat as needing to load new data

    
    # ---------------