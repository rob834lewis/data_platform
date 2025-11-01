# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07SEP2025

    Purpose         : Global variables for environment setup

    Dependencies    :

    Program name    : globals

    Modifications
    -------------
    07SEP2025   RLEWIS  Initial Version 
    27OCT2025   RLEWIS  Updated to work in Windows
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import sys
from pathlib import Path
   
# ------------------------
# --- Global variables ---
# ------------------------

current_file      = Path(__file__).resolve()
project_root_name = "data-coven"

# Look through all parent folders
project_root = next((p for p in current_file.parents if p.name == project_root_name), None)

if project_root is None:
    raise RuntimeError(f"Could not find {project_root_name} in path hierarchy")

# add the common directory to sys.path
sys.path.append(str(project_root)+'\\src')

# thus enabling import of autoexec file
from common.autoexec import *