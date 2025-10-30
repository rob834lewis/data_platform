# run_airflow.ps1 - Portable version for subfolder

# Get the script's directory (scripts folder)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Assume project root is the parent of the scripts folder
$projectRoot = Split-Path $scriptDir -Parent
Set-Location $projectRoot
Write-Host "Changed working directory to project root: $projectRoot"

# Load environment variables from .env in project root
$envFile = Join-Path $projectRoot ".env"
Write-Host "Loading environment variables from $envFile"

# Define required environment variables
$requiredVars = @(
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "AIRFLOW_ADMIN_USER",
    "AIRFLOW_ADMIN_FIRSTNAME",
    "AIRFLOW_ADMIN_LASTNAME",
    "AIRFLOW_ADMIN_EMAIL",
    "AIRFLOW_ADMIN_PASSWORD"
)

# Load .env file
if (-Not (Test-Path $envFile)) {
    throw "Env file '$envFile' does not exist."
}

Get-Content $envFile | ForEach-Object {
    # Ignore empty lines or comments
    if ($_ -and $_ -notmatch "^\s*#") {
        $parts = $_ -split "=", 2
        if ($parts.Count -ne 2) { throw "Invalid line in .env file: $_" }
        $name = $parts[0].Trim()
        $value = $parts[1].Trim()

        # Set in both Process environment and $env: for PowerShell
        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        ${env:$name} = $value
    }
}

# Verify that all required variables are set
foreach ($var in $requiredVars) {
    $envValue = [System.Environment]::GetEnvironmentVariable($var, "Process")
    if (-not $envValue) {
        throw "Required environment variable '$var' is missing. Please add it to $envFile."
    }
}

# 1. Clean up previous runs
Write-Host "--- DOWN: Cleaning up previous runs ---"
docker compose down -v

# 2. Initialize Airflow
Write-Host "--- INIT: Running DB Migration and User Creation ---"
docker compose run airflow-init

# 3. Set Admin User
Write-Host "--- ADMIN: Creating Airflow admin user ---"
docker compose run --rm airflow-webserver airflow users create `
  --username $env:AIRFLOW_ADMIN_USER `
  --firstname $env:AIRFLOW_ADMIN_FIRSTNAME `
  --lastname $env:AIRFLOW_ADMIN_LASTNAME `
  --role Admin `
  --email $env:AIRFLOW_ADMIN_EMAIL `
  --password $env:AIRFLOW_ADMIN_PASSWORD

# 4. Start all services
Write-Host "--- UP: Starting Airflow Services ---"
docker compose up -d

Write-Host "--- DONE: Check containers with 'docker compose ps' ---"
