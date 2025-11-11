#!/usr/bin/env bash
set -euo pipefail

echo "Render build script: starting"

# Upgrade pip and install requirements if present
if [ -f requirements.txt ]; then
  echo "Installing Python dependencies from requirements.txt..."
  python -m pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "No requirements.txt found — skipping pip install"
fi

# Collect static files (Render expects this during build)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations if a DATABASE_URL is provided (optional)
if [ -n "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL detected — running migrations"
  python manage.py migrate --noinput || true
else
  echo "No DATABASE_URL detected — skipping migrations"
fi

echo "Render build script: finished"
