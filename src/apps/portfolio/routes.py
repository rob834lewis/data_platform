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

from flask       import Blueprint, render_template

        # ---------------

# ------------
# --- Main ---
# ------------


portfolio_bp = Blueprint('portfolio', __name__, template_folder='templates')


@portfolio_bp.route('/')
def index():
    """
    Home page for the portfolio
    Links to other apps / pages like the top 10 exchange rates
    """
    return render_template('index.html', title="Data Coven | Home")

        # ---------------