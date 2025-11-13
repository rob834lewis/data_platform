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
    09NOV2025   RLEWIS  Added db_url
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os
from dotenv      import load_dotenv
from src.globals import *

        # ---------------

load_dotenv()

# -------------
# --- Class ---
# -------------

class Config:

    db_url = (
            f"postgresql+psycopg2://{current_db['user']}:{current_db['password']}"
            f"@{current_db['host']}:{current_db['port']}/{current_db['dbname']}?sslmode={current_db['sslmode']}"
        )


    SECRET_KEY                     = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI        = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

        # ---------------