# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
  Written by      : Rob Lewis

  Date            : 02NOV2025

  Purpose         : Create directory if it doesn't exist

  Dependencies    :

  Module name     : ensure_directory_exists

  Modifications
  -------------
  02NOV2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals import *
from .get_logger import get_logger

# ----------------
# --- Function ---
# ----------------

# create directory if it doesn't exist
def ensure_directory_exists(path_string: str) -> None:
    """
    Checks if a directory exists at the given path string, and creates it 
    (along with any necessary parent directories) if it doesn't.
    """
    if not os.path.exists(path_string):

        # os.makedirs creates all intermediate directories needed.
        try:
            os.makedirs(path_string)
            logging.info(f"Created directory: {path_string}")

        except OSError as e:

            # Handle potential permission errors or other system issues
            logging.info(f"Error creating directory {path_string}: {e}")
            raise