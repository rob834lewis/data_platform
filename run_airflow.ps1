# run_airflow.ps1 - Simpler PowerShell script using --env-file flag

$envFile = "docker-compose-variables.env"

# 1. Clean up previous runs
Write-Host "--- DOWN: Cleaning up previous runs ---"
docker compose down -v

# 2. Initialize Airflow
Write-Host "--- INIT: Running DB Migration and User Creation ---"
# We explicitly pass the env file to the 'run' command
docker compose --env-file $envFile run --rm airflow-init

# 3. Start all services
Write-Host "--- UP: Starting Airflow Services ---"
# We explicitly pass the env file to the 'up' command
docker compose --env-file $envFile up -d

Write-Host "--- DONE: Check containers with 'docker compose ps' ---"