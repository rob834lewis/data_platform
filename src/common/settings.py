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
    28OCT2025   RLEWIS  Removed normalised_path and read file content, add platform and db details
    29OCT2025   RLEWIS  Added dotenv
    01NOV2025   RLEWIS  Updated project root logic to account for movement of code to src
    02NOV2025   RLEWIS  Added docker db setting
    09NOV2025   RLEWIS  Updated with Azure and app settings
-------------------------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os, socket, dateutil.parser, platform, requests
from pathlib import Path
from dotenv import load_dotenv
import boto3
import json

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

# function to detect which OS is being run
def detect_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "local_windows"
    elif os_name == "Linux":
        return "linux"
    elif os_name == "Darwin":
        return "macos"
    return "unknown_os"

# detect which cloud is being used 
import requests

def detect_cloud():
    try:
        # GCP metadata server
        resp = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"},
            timeout=0.1
        )
        if resp.status_code == 200:
            return "gcp"
    except requests.exceptions.RequestException:
        pass

    try:
        # AWS metadata server
        token_resp = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=1
        )
        token = token_resp.text

        resp = requests.get("http://169.254.169.254/latest/meta-data/", headers={"X-aws-ec2-metadata-token": token}, timeout=1)
        if resp.status_code == 200:
            return "aws"
    except requests.exceptions.RequestException:
        pass

    try:
        # Azure metadata server
        resp = requests.get(
            "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
            headers={"Metadata": "true"},
            timeout=0.1
        )
        if resp.status_code == 200:
            return "azure"
    except requests.exceptions.RequestException:
        pass

    return "local_or_unknown"

# function to detect which environment is being used
# -> "local_windows", "gcp", "aws", "azure", etc.
def detect_environment():
    os_env    = detect_os()
    cloud_env = detect_cloud()

    if cloud_env != "local_or_unknown":
        return cloud_env
    
    return os_env

# Pass ddmonyyyy to date akin to SAS date9. format    
def d(dte):
    return dateutil.parser.parse(dte).date()

# create directory if it doesn't exist
def ensure_directory_exists(path_string: str) -> None:
    """
    Checks if a directory exists at the given path string, and creates it 
    (along with any necessary parent directories) if it doesn't.
    """
    if not os.path.exists(path_string):
        # os.makedirs creates all intermediate directories needed.
        # exist_ok=True (if you were using pathlib) is implicitly handled
        # by checking os.path.exists first.
        try:
            os.makedirs(path_string)
            print(f"Created directory: {path_string}")
        except OSError as e:
            # Handle potential permission errors or other system issues
            print(f"Error creating directory {path_string}: {e}")
            raise


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

# ------------------------
# --- File Directories ---
# ------------------------

# Set a fallback/default value
project_root_env_var = os.environ.get("PROJECT_ROOT")

if project_root_env_var:

    # Use the path defined in the Docker Compose environment
    project_root = project_root_env_var

else:

    # obtain current file information
    try:
        current_file = Path(__file__).resolve()

    except NameError:
        current_file = Path.cwd()

    # Assume project root name
    project_root_name = "data-coven"

    # Look through all parent folders
    project_root = next( (p for p in [current_file] + list(current_file.parents) if p.name == project_root_name), None)

    if project_root is None:
        raise RuntimeError(f"Could not find {project_root_name} in path hierarchy")

# log directory
log_dir = os.path.join(project_root,"src","logs")
ensure_directory_exists(log_dir) # Create folder if missing

# data directory
data_dir = os.path.join(project_root,"src","data")
ensure_directory_exists(data_dir) # Create folder if missing

# ---
# env variables
# ---

# Load env
env_file = os.path.join(project_root,".env")
loaded_dotenv = load_dotenv(dotenv_path=env_file)

# ---
# server details
# ---

hostname, ip_address = get_server_info()

# ------------------------
# --- Database Options ---
# ------------------------

# THE CLOUD DETAILS BELOW IS JUST A DUMMY PLACEHOLDER
# WILL NEED TO USE SECRET MANAGERS WHEN ACTUALLY USING CLOUD

# Local Postgres
db_config_local = {
    "host"    : os.environ.get("DB_HOST_LOCAL"),
    "port"    : os.environ.get("DB_PORT_LOCAL"),
    "dbname"  : os.environ.get("DB_NAME_LOCAL"),
    "user"    : os.environ.get("DB_USER_LOCAL"),
    "password": os.environ.get("DB_PASS_LOCAL"),
    "sslmode" : os.environ.get("DB_SSLM_LOCAL")
}

# Docker Postgres
db_config_docker = {
    "host"    : os.environ.get("POSTGRES_HOST_DOCKER"),
    "dbname"  : os.environ.get("POSTGRES_DB"),
    "user"    : os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD")
}

# --------------------------
# --- GCP / Cloud SQL Postgres
# --------------------------
db_config_gcp = {
    "host": "34.123.45.67",  # Cloud SQL public IP or private IP
    "dbname": "exchange_rates",
    "user": "gcp_user",
    "password": "gcp_password",
    "sslmode": "require"      # if using SSL
}

# --------------------------
# --- Azure / PostgreSQL Flexible Server
# --------------------------
db_config_azure = {
    "host"    : os.environ.get("DB_HOST_AZURE"),
    "port"    : os.environ.get("DB_PORT_AZURE"),
    "dbname"  : os.environ.get("DB_NAME_AZURE"),
    "user"    : os.environ.get("DB_USER_AZURE"),
    "password": os.environ.get("DB_PASS_AZURE"),
    "sslmode" : os.environ.get("DB_SSLM_AZURE")
}

# if running locally
if detect_environment() == 'local_windows':

    current_db = db_config_local
    app_host   = os.environ.get("APP_HOST_LOCAL")
    app_dbug   = os.environ.get("APP_DBUG_LOCAL")

elif detect_environment() == 'aws':

    # --------------------------
    # --- AWS / RDS Postgres
    # --------------------------

    secret_name = "rds!db-6e4e1293-907d-4132-aa4d-21b33c883d07"
    region_name = "eu-north-1"

    client = boto3.client('secretsmanager', region_name=region_name)
    secret = client.get_secret_value(SecretId=secret_name)

    # The secret string is a JSON string
    secret_json = secret["SecretString"]

    # Convert JSON string to Python dictionary
    secret_dict = json.loads(secret_json)

    db_config_aws = {
        "host"    : os.environ.get("DB_HOST_AWS") ,
        "dbname"  : os.environ.get("DB_NAME_AWS") ,
        "user"    : secret_dict["username"]       ,
        "password": secret_dict["password"]       ,
        "port"    : os.environ.get("DB_PORT_AWS") ,
        "sslmode" : os.environ.get("DB_SSLM_AWS")
    }

    current_db = db_config_aws
    app_host   = os.environ.get("APP_HOST_CLOUD")
    app_dbug   = os.environ.get("APP_DBUG_CLOUD")

elif detect_environment() == 'azure':

    current_db = db_config_azure
    app_host   = os.environ.get("APP_HOST_CLOUD")
    app_dbug   = os.environ.get("APP_DBUG_CLOUD")

elif detect_environment() == 'gcp':

    current_db = db_config_azure
    app_host   = os.environ.get("APP_HOST_CLOUD")
    app_dbug   = os.environ.get("APP_DBUG_CLOUD")

    gcp_project = "data-coven-dev"
    gcp_bucket  = "data-coven-dev-eu-west2-001" 

# else if running in docker 
elif project_root_env_var:

    current_db = db_config_docker

else:

    current_db = None
