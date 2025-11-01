# -------------------------------------------------------------------------------------------------------------------
#    Written by      : Rob Lewis
#
#    Date            : 07SEP2025
#
#    Purpose         : Main terraform setup script
#
#    Dependencies    :
#
#    Program name    : main
#
#    Modifications
#    -------------
#    07SEP2025   RLEWIS  Initial Version
#    14SEP2025   RLEWIS  Altered for use with multiple projects for each environment
# ------------------------------------------------------------------------------------------------------------------- 


terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ---------------------------
# Create bucket for environment
# ---------------------------
resource "google_storage_bucket" "bucket" {
  name     = "${var.project_id}-eu-west2-001"
  location = "EUROPE-WEST2"

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  # PROD retention dynamically applied
  dynamic "retention_policy" {
    for_each = var.environment == "prd" ? [1] : []

    content {
      retention_period = var.prod_retention_days * 86400
    }
  }

  # DEV lifecycle rule for temp folder
  dynamic "lifecycle_rule" {
    for_each = var.environment == "dev" ? [1] : []

    content {
      action {
        type = "Delete"
      }
      condition {
        age            = 30
        matches_prefix = ["temp/"]
      }
    }
  }
}

# ---------------------------
# Create folder placeholders
# ---------------------------
resource "google_storage_bucket_object" "folders" {
  for_each = toset(var.folders)

  name   = "${each.key}/.keep"
  bucket = google_storage_bucket.bucket.name
  source = "empty.txt" # zero-byte file to create the folder
}
