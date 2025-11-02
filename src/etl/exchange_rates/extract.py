# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Extract step for Exchange Rates 

    Dependencies    :

    Program name    : extract

    Modifications
    -------------
    27OCT2025   RLEWIS  Initial Version
    02NOV2025   RLEWIS  File date is now taken from the data
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals          import *
from src.common.functions import wdays, get_logger, ensure_directory_exists

# ---------------
# --- Logging ---
# ---------------

logger = get_logger("exchange_rates")
    
    # ---------------

# ----------------
# --- Function ---
# ----------------

def extract(url: str, ns: str) -> Path:

    """
    Fetch ECB XML and save to raw folder.
    
    Returns
    -------
    Path
        Path to the saved raw XML file.
    """

    logger.info("Extracting daily exchange rates from ECB API")

    # --- Make request ---
    resp = requests.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    # Extract the date from the XML
    cube = root.find(".//ns:Cube[@time]", ns)
    xml_date = pd.to_datetime(cube.attrib.get("time")).strftime("%Y%m%d")

    # Build raw filename    
    raw_filename = f"ecb_rates_{xml_date}.xml"

    # Build Local & Airflow path
    base_dir = os.path.join(data_dir, "ecb_daily_rates", "raw")
    ensure_directory_exists(base_dir) # Create folder if missing

    raw_path = os.path.join(base_dir, raw_filename)

    # Save raw ECB rates to file
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
        
    logger.info(f"Saved raw XML to {raw_path}")

    """

raw_prefix     = "raw/exchange_rates/"     # Folder (prefix) in bucket for raw files
staging_prefix = "staging/exchange_rates/" # Folder for cleaned, intermediate CSV

"""



    return raw_path
