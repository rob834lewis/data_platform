# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 06NOV2025

    Purpose         : 

    Dependencies    :

    Program name    : routes

    Modifications
    -------------
    06NOV2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from src.globals               import *
from flask                     import Flask
from src.apps.portfolio.routes import main
        
        # ---------------

# ------------
# --- Main ---
# ------------

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app