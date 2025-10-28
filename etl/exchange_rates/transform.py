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
def transform(raw_path: Path) -> pd.DataFrame:
    
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

    # ECB XML namespaces
    ns = {
        "ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
    }

    # Extract date and rates
    cube = root.find(".//ecb:Cube/ecb:Cube", ns)
    date = cube.attrib.get("time")

    # Build list of dicts
    data = []
    for currency_node in cube.findall("ecb:Cube", ns):
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
    staging_dir = data_dir / "ecb_daily_rates" / "staging"
    staging_dir.mkdir(parents=True, exist_ok=True)

    staging_file = staging_dir / f"ecb_rates_staging_{today}.csv"
    df.to_csv(staging_file, index=False)

    logger.info(f"Staging CSV saved to {staging_file}")

    return df