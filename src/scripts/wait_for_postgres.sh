#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -p 5432 -U "$POSTGRES_USER"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is ready, starting Airflow..."
exec "$@"
