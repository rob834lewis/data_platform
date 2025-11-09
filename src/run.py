# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 06NOV2025

    Purpose         : 

    Dependencies    :

    Program name    : run

    Modifications
    -------------
    06NOV2025   RLEWIS  Initial Version
    09NOV2025   RLEWIS  Added app vars
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------
 
from src.globals        import *
from src.apps.portfolio import create_app

        # ---------------

# Call the factory function to create the Flask app instance
app = create_app()

# Check if this file is being run directly
if __name__ == "__main__":
    
    # start server
    app.run(debug=app_dbug, host=f"{app_host}", port=5000)
