# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 27OCT2025

    Purpose         : Transform step for Exchange Rates 

    Dependencies    :

    Program name    : transform

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
def transform(ns: dict, raw_path: Path) -> pd.DataFrame:
    
    """
    Transform ECB XML data into a Pandas DataFrame and save a staging CSV.
    
    Parameters
    ----------
    raw_path : Path
        Path to the raw XML file.
        
    Returns
    -------
    pd.DataFrame
        Transformed data ready for load.
    """
    
    logger.info(f"Transforming raw XML: {raw_path}")

    # --- Parse XML ---
    tree = ET.parse(raw_path)
    root = tree.getroot()

    # Extract date and rates
    cube_time = root.find(".//ns:Cube[@time]", ns)
    if cube_time is None:
        raise ValueError("No <Cube time=...> element found in XML. Check namespace or structure.")
    date = cube_time.attrib.get("time")
    xmldsn = pd.to_datetime(cube_time.attrib.get("time")).strftime("%Y%m%d")

    # Build list of dicts
    data = []
    for currency_node in cube_time.findall("ns:Cube", ns):
        data.append({
            "date": date,
            "currency": currency_node.attrib["currency"],
            "rate": float(currency_node.attrib["rate"])
        })

    # Add EUR as base
    data.append({"date": date, "currency": "EUR", "rate": 1.0})

    # --- Convert to DataFrame ---
    df = pd.DataFrame(data)

    # --- Save staging CSV ---
    staging_dir = os.path.join(data_dir, "ecb_daily_rates", "staging")
    ensure_directory_exists(staging_dir) # Create folder if missing

    staging_file = os.path.join(staging_dir, f"ecb_rates_staging_{xmldsn}.csv")
    df.to_csv(staging_file, index=False)

    logger.info(f"Staging CSV saved to {staging_file}")

    return df