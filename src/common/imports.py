# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07SEP2025

    Purpose         : Store all main imports in one place

    Dependencies    :

    Program name    : imports

    Modifications
    -------------
    07SEP2025   RLEWIS  Initial Version
    14SEP2025   RLEWIS  Added bigquery & pandas_gbq imports
    28OCT2025   RLEWIS  Added psycopg2
    02NOV2025   RLEWIS  Added sys
    09NOV2025   RLEWIS  Added sqlalchemy
    25NOV2025   RLEWIS  Added time
    27NOV2025   RLEWIS  Added additional descriptions
---------------------------------------------------------------------------------------------------
"""


# ---------------
# --- Imports ---
# ---------------

import pandas as pd                 # For data manipulation
import numpy  as np                 # For scientific calculations
import requests                     # For making HTTP requests
import xml.etree.ElementTree as ET  # For parsing XML files
import logging                      # For creating logs
import sys                          # For accessing system-specific parameters and functions
import pandas_gbq                   # For interacting with Google BigQuery using pandas
import psycopg2                     # For connecting to PostgreSQL databases
import time                          # For time-related functions (sleep, timestamps, etc.)

from sqlalchemy import create_engine, text, Table, Column, Date, String, Float, MetaData  # For SQLAlchemy ORM and database schema definitions
from sqlalchemy.dialects.postgresql import insert                                         # For PostgreSQL-specific insert operations

from google.cloud           import storage, bigquery          # For interacting with Google Cloud Storage (GCS) and bigquery
from datetime               import datetime, date, timedelta  # For generating dates
from dateutil.relativedelta import relativedelta              # For working with timedeltas
