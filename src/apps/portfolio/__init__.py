# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 06NOV2025

    Purpose         : app factory and initialiser for portfolio web app

    Dependencies    :

    Program name    : __init__

    Modifications
    -------------
    06NOV2025   RLEWIS  Initial Version
    07NOV2025   RLEWIS  Updated create_app and annotated
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from flask   import Flask
from .db     import db
from .config import Config
from .routes import portfolio_bp
from src.apps.exchange_rates.routes import exchange_bp
        
"""

Flask        : the main Flask class that creates a web application.

portfolio_bp : the Blueprint defined in routes.py that holds all the / route(s).

db           : the SQLAlchemy database object. This is used to connect the Flask app to Postgres.

Config       : a class that holds the app configuration — database URI, secret key, etc.


"""

        # ---------------

# ------------
# --- Main ---
# ------------

def create_app():

    """
    
    a factory function to create and return a new Flask app
    
    """

    # initializes the Flask app instance
    app = Flask(__name__) 

    # load settings from Config
    app.config.from_object(Config) 
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(exchange_bp) 
    
    return app