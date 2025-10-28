# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 11SEP2025

    Purpose         : Settings file to store the global variables

    Dependerncies   :

    Program name    : settings

    Modifications
    -------------
    11SEP2025   RLEWIS  Initial Version 
    14SEP2025   RLEWIS  Updated dev gcp bucket name
    28OCT2025   RLEWIS  Removed normalised_path and read file content
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os, socket, dateutil.parser
from pathlib import Path
   
# -----------------
# --- Functions ---
# -----------------

# function to retrieve details of the current server
def get_server_info():
    try:
        # Get the hostname
        hostname = socket.gethostname()
        # Resolve the hostname to an IP address
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except Exception as e:
        return f"Error: {e}"

# Pass ddmonyyyy to date akin to SAS date9. format    
def d(dte):
    return dateutil.parser.parse(dte).date()

# -------------------------------
# --- Global variables
# -------------------------------

# Bank Holiday set
set_bank_hols = set([
    d("03JAN2000"),d("21APR2000"),d("24APR2000"),d("01MAY2000"),d("29MAY2000"),d("28AUG2000"),d("25DEC2000"),d("26DEC2000"),
    d("01JAN2001"),d("13APR2001"),d("16APR2001"),d("07MAY2001"),d("28MAY2001"),d("27AUG2001"),d("25DEC2001"),d("26DEC2001"),
    d("01JAN2002"),d("29MAR2002"),d("01APR2002"),d("06MAY2002"),d("03JUN2002"),d("04JUN2002"),d("26AUG2002"),d("25DEC2002"),d("26DEC2002"),
    d("01JAN2003"),d("18APR2003"),d("21APR2003"),d("05MAY2003"),d("26MAY2003"),d("25AUG2003"),d("25DEC2003"),d("26DEC2003"),
    d("01JAN2004"),d("09APR2004"),d("12APR2004"),d("03MAY2004"),d("31MAY2004"),d("30AUG2004"),d("27DEC2004"),d("28DEC2004"),
    d("03JAN2005"),d("25MAR2005"),d("28MAR2005"),d("02MAY2005"),d("30MAY2005"),d("29AUG2005"),d("26DEC2005"),d("27DEC2005"),
    d("02JAN2006"),d("14APR2006"),d("17APR2006"),d("01MAY2006"),d("29MAY2006"),d("28AUG2006"),d("25DEC2006"),d("26DEC2006"),
    d("01JAN2007"),d("06APR2007"),d("09APR2007"),d("07MAY2007"),d("28MAY2007"),d("27AUG2007"),d("25DEC2007"),d("26DEC2007"),
    d("01JAN2008"),d("21MAR2008"),d("24MAR2008"),d("05MAY2008"),d("26MAY2008"),d("25AUG2008"),d("25DEC2008"),d("26DEC2008"),
    d("01JAN2009"),d("10APR2009"),d("13APR2009"),d("04MAY2009"),d("25MAY2009"),d("31AUG2009"),d("25DEC2009"),d("26DEC2009"),
    d("01JAN2010"),d("02APR2010"),d("05APR2010"),d("03MAY2010"),d("31MAY2010"),d("30AUG2010"),d("27DEC2010"),d("28DEC2010"),
    d("03JAN2011"),d("22APR2011"),d("25APR2011"),d("29APR2011"),d("02MAY2011"),d("30MAY2011"),d("29AUG2011"),d("26DEC2011"),d("27DEC2011"),
    d("02JAN2012"),d("06APR2012"),d("09APR2012"),d("07MAY2012"),d("04JUN2012"),d("05JUN2012"),d("27AUG2012"),d("25DEC2012"),d("26DEC2012"),
    d("01JAN2013"),d("29MAR2013"),d("01APR2013"),d("06MAY2013"),d("27MAY2013"),d("26AUG2013"),d("25DEC2013"),d("26DEC2013"),
    d("01JAN2014"),d("18APR2014"),d("21APR2014"),d("05MAY2014"),d("26MAY2014"),d("25AUG2014"),d("25DEC2014"),d("26DEC2014"),
    d("01JAN2015"),d("03APR2015"),d("06APR2015"),d("04MAY2015"),d("25MAY2015"),d("31AUG2015"),d("25DEC2015"),d("28DEC2015"),
    d("01JAN2016"),d("25MAR2016"),d("28MAR2016"),d("02MAY2016"),d("30MAY2016"),d("29AUG2016"),d("26DEC2016"),d("27DEC2016"),
    d("02JAN2017"),d("14APR2017"),d("17APR2017"),d("01MAY2017"),d("29MAY2017"),d("28AUG2017"),d("25DEC2017"),d("26DEC2017"),
    d("01JAN2018"),d("30MAR2018"),d("02APR2018"),d("07MAY2018"),d("28MAY2018"),d("27AUG2018"),d("25DEC2018"),d("26DEC2018"),
    d("01JAN2019"),d("19APR2019"),d("22APR2019"),d("06MAY2019"),d("27MAY2019"),d("26AUG2019"),d("25DEC2019"),d("26DEC2019"),
    d("01JAN2020"),d("10APR2020"),d("13APR2020"),d("08MAY2020"),d("25MAY2020"),d("31AUG2020"),d("25DEC2020"),d("28DEC2020"),
    d("01JAN2021"),d("02APR2021"),d("05APR2021"),d("03MAY2021"),d("31MAY2021"),d("30AUG2021"),d("27DEC2021"),d("28DEC2021"),
    d("03JAN2022"),d("15APR2022"),d("18APR2022"),d("02MAY2022"),d("02JUN2022"),d("03JUN2022"),d("29AUG2022"),d("26DEC2022"),d("27DEC2022"),
    d("02JAN2023"),d("07APR2023"),d("10APR2023"),d("01MAY2023"),d("08MAY2023"),d("29MAY2023"),d("28AUG2023"),d("25DEC2023"),d("26DEC2023"),    
    d("01JAN2024"),d("29MAR2024"),d("01APR2024"),d("06MAY2024"),d("27MAY2024"),d("26AUG2024"),d("25DEC2024"),d("26DEC2024"),    
    d("01JAN2025"),d("18APR2025"),d("21APR2025"),d("05MAY2025"),d("26MAY2025"),d("25AUG2025"),d("25DEC2025"),d("26DEC2025"),
    d("01JAN2026"),d("03APR2026"),d("06APR2026"),d("04MAY2026"),d("25MAY2026"),d("31AUG2026"),d("25DEC2026"),d("28DEC2026"),
    d("01JAN2027"),d("26MAR2027"),d("29MAR2027"),d("03MAY2027"),d("31MAY2027"),d("30AUG2027"),d("27DEC2027"),d("28DEC2027"),
    d("03JAN2028"),d("14APR2028"),d("17APR2028"),d("01MAY2028"),d("29MAY2028"),d("28AUG2028"),d("25DEC2028"),d("26DEC2028"),    
    d("01JAN2029"),d("30MAR2029"),d("02APR2029"),d("05MAY2029"),d("28MAY2029"),d("27AUG2029"),d("25DEC2029"),d("26DEC2029"),  
    d("01JAN2030"),d("19APR2030"),d("22APR2030"),d("06MAY2030"),d("27MAY2030"),d("28AUG2030"),d("25DEC2030"),d("26DEC2030"),  
])

# server details
hostname, ip_address = get_server_info()

# gcp details
# <WILL NEED TO INCLUDE CHECK ON ENVIRONMENT HERE DEV,UAT OR PROD>
gcp_project = "data-coven-dev"
gcp_bucket  = "data-coven-dev-eu-west2-001"  # Your GCS bucket name

# ------------------------
# --- File Directories ---
# ------------------------

current_file      = Path(__file__).resolve()
project_root_name = "data-coven"

# Look through all parent folders
project_root = next((p for p in current_file.parents if p.name == project_root_name), None)

# log directory
log_dir = project_root / "logs"
log_dir.mkdir(parents=True, exist_ok=True)  # Create folder if missing

# data directory
data_dir = project_root / "data"
data_dir.mkdir(parents=True, exist_ok=True)  # Create folder if missing