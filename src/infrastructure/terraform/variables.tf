# -------------------------------------------------------------------------------------------------------------------
#    Written by      : Rob Lewis
#
#    Date            : 07SEP2025
#
#    Purpose         : Variables for use in terraform setup
#
#    Dependencies    :
#
#    Program name    : variables
#
#    Modifications
#    -------------
#    07SEP2025   RLEWIS  Initial Version
#    14SEP2025   RLEWIS  Altered for use with multiple projects for each environment
# ------------------------------------------------------------------------------------------------------------------- 

variable "project_id" {
  type        = string
  description = "GCP Project ID for this environment"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "europe-west2"
}

variable "environment" {
  type        = string
  description = "Environment name: dev, uat, prd"
}

variable "folders" {
  type        = list(string)
  description = "Folder structure inside the bucket"
  default     = ["archive", "output", "raw", "staging", "temp"]
}

variable "prod_retention_days" {
  type        = number
  description = "Retention period for PROD bucket in days"
  default     = 30
}
