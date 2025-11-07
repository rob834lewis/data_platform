# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07NOV2025

    Purpose         : app factory and initialiser for portfolio web app

    Dependencies    :

    Program name    : config

    Modifications
    -------------
    07NOV2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os
from dotenv import load_dotenv

        # ---------------

load_dotenv()

# -------------
# --- Class ---
# -------------

class Config:

    SECRET_KEY                     = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI        = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

        # ---------------