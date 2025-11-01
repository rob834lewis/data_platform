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
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os, sys

# -----------------
# --- Functions ---
# -----------------

# function to return true normalised path
def normalised_path(path):
    if path == "//":
        return "/"
    elif path.startswith("//"):
        return os.path.normpath(os.path.dirname(path))[1:]
    else:
        return os.path.normpath(os.path.dirname(path))
    
# ------------------------
# --- Global variables ---
# ------------------------

# path obtained from current file
project_root = normalised_path(__file__)

# split the file path into its components
project_root = project_root.split(os.sep)

# first two levels
project_root = os.sep.join(project_root[0:3])

# add the common directory to sys.path
sys.path.append(project_root)

# thus enabling import of autoexec file
from common.autoexec import *