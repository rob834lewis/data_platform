# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07NOV2025

    Purpose         : Central database connection placeholder for Flask app; db is initialised with app in __init__.py

    Dependencies    :

    Program name    : db

    Modifications
    -------------
    07NOV2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from flask_sqlalchemy import SQLAlchemy

        # ---------------

# ------------
# --- Main ---
# ------------

# create SQLAlchemy object
db = SQLAlchemy()

        # ---------------
