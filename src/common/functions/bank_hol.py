# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
  Written by      : Rob Lewis

  Date            : 11SEP2025

  Purpose         : Build Bank Holiday Field

  Dependencies    :

  Module name    : bank_hol

  Modifications
  -------------
  11SEP2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from globals import *

# ----------------
# --- Function ---
# ----------------

def bank_hol(cell_date):

    global set_bank_hols

    if cell_date in set_bank_hols:
        return 'Y'
    else:
        return 'N'