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
  14SEP2025   RLEWIS  Updated log dir call
  27OCT2025   RLEWIS  Added wdays
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from globals import *
from .wdays  import wdays

# ----------

# ----------------------
# --- Date Variables ---
# ----------------------

todays_date = wdays().get("todays_date")

# ----------

# ----------------
# --- Function ---
# ----------------

def get_logger(name: str, log_dir: str = log_dir) -> logging.Logger:
    """Return a logger that writes to both console and rotating file."""
    # Ensure the log folder exists
    os.makedirs(log_dir, exist_ok=True)
    logfile = os.path.join(log_dir, f"{name}_{todays_date}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler (INFO and above)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    # File handler (DEBUG and above)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

# ----------