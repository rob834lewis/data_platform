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

raw_file = extract()
df       = transform(raw_file)
print(df.head())