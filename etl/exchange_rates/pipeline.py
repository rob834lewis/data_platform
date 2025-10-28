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
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals                      import *
from etl.exchange_rates.extract   import extract
from etl.exchange_rates.transform import transform
from etl.exchange_rates.load      import load

# Step 1: Extract
raw_file = extract()

# Step 2: Transform
df = transform(raw_file)

# Step 3: Load
load(df)