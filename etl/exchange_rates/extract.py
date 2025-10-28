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

from globals          import *
from common.functions import wdays, get_logger

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

def extract() -> Path:

    """
    Fetch ECB XML and save to raw folder.
    
    Returns
    -------
    Path
        Path to the saved raw XML file.
    """

    ecb_xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

    logger.info("Extracting daily exchange rates from ECB API")

    # --- Make request ---
    resp = requests.get(ecb_xml_url)
    resp.raise_for_status()

    # --- Build path ---
    base_dir = data_dir / "ecb_daily_rates" / "raw"
    base_dir.mkdir(parents=True, exist_ok=True)

    raw_filename = f"ecb_rates_{today}.xml"
    raw_path = base_dir / raw_filename

    # --- Save response text to file ---
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(resp.text)

    logger.info(f"Saved raw XML to {raw_path}")

    return raw_path
