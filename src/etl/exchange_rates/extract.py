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

# ----------------------
# --- Date Variables ---
# ----------------------

today = wdays().get("today")
    
    # ---------------

# ----------------
# --- Function ---
# ----------------

def extract(url: str) -> Path:

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

    # --- Build path ---
    base_dir = os.path.join(data_dir, "ecb_daily_rates", "raw")
    ensure_directory_exists(base_dir) # Create folder if missing

    raw_filename = f"ecb_rates_{today}.xml"
    raw_path = os.path.join(base_dir, raw_filename)

    # --- Save response text to file ---
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(resp.text)

    logger.info(f"Saved raw XML to {raw_path}")

    return raw_path
