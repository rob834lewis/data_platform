# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
  Written by      : Rob Lewis

  Date            : 11SEP2025

  Purpose         : Upload data into GCS buckets

  Dependencies    :

  Module name    : upload_to_gcs

  Modifications
  -------------
  11SEP2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from globals import *

# ----------------
# --- Function ---
# ----------------

# Helper function to upload files to GCS
def upload_to_gcs(bucket, prefix, filename, content):

    client = storage.Client()                                  # Create a GCS client (auth comes from environment)
    blob = client.bucket(bucket).blob(prefix + filename)       # Point to the object path inside the bucket
    blob.upload_from_string(content, content_type="text/csv")  # Upload string content as CSV
    return f"gs://{bucket}/{prefix}{filename}"                 # Return the GCS path (for logging/debug)