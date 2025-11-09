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
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------
 
from src.apps.portfolio import create_app

        # ---------------

# Call the factory function to create the Flask app instance
app = create_app()

# Check if this file is being run directly
if __name__ == "__main__":
    
    # start server
    app.run(debug=True, host="0.0.0.0", port=5000)
