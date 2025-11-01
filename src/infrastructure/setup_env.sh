#!/usr/bin/env bash
# -------------------------------------------------------------------------------------------------------------------
# Written by      : Rob Lewis DO NOT RUN YET THIS NEEDS REVIEWING FIRST!!!!!!
# Date            : 14SEP2025
# Purpose         : Spin up a GCP environment (Terraform + bucket folders)
# Dependencies    : Terraform installed, gcloud auth set up
# -------------------------------------------------------------------------------------------------------------------

# Exit immediately if a command fails
set -e

# ---------------------------
# --- CONFIGURATION ---------
# ---------------------------

# Environment: dev | uat | prd
ENVIRONMENT=${1:-dev}

# Corresponding GCP project
declare -A PROJECTS
PROJECTS=( ["dev"]="data-coven-dev" ["uat"]="data-coven-uat" ["prd"]="data-coven-prd" )

PROJECT_ID=${PROJECTS[$ENVIRONMENT]}

# Terraform folder (relative to this script)
TERRAFORM_DIR="./terraform"

echo "🚀 Setting up environment: $ENVIRONMENT"
echo "Using GCP project: $PROJECT_ID"

# ---------------------------
# --- TERRAFORM INIT & APPLY
# ---------------------------

cd "$TERRAFORM_DIR"

echo "🔹 Initializing Terraform..."
terraform init

echo "🔹 Planning Terraform for $ENVIRONMENT..."
terraform plan -var="project_id=$PROJECT_ID" -var="environment=$ENVIRONMENT"

echo "🔹 Applying Terraform..."
terraform apply -auto-approve -var="project_id=$PROJECT_ID" -var="environment=$ENVIRONMENT"

echo "Terraform completed for $ENVIRONMENT"

# ---------------------------
# --- OPTIONAL: POST-PROVISIONING
# ---------------------------

# Example: upload an empty.txt to each folder if you want to re-seed buckets
# (you could call a Python script here if needed)
# python3 ../../scripts/seed_buckets.py --env $ENVIRONMENT
# make it executable
# chmod +x infrastructure/setup_env.sh
# run it for a specific environment
# ./infrastructure/setup_env.sh dev

echo "🎉 Environment setup completed: $ENVIRONMENT"

