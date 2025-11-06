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

from src.globals import *
from flask       import Blueprint, render_template

        # ---------------

# ------------
# --- Main ---
# ------------

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Data Coven')

        # ---------------