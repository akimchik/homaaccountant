#!/bin/bash

# This script resets the Django database by deleting the existing SQLite file
# and migration history, then reapplies all migrations.
# WARNING: This will permanently delete all data in your database.

# Deactivate virtual environment if active
if command -v deactivate &> /dev/null
then
    deactivate
fi

echo "Deleting existing database file (db.sqlite3)..."
rm -f db.sqlite3

echo "Deleting migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "Recreating virtual environment and installing dependencies..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install Django

echo "Applying new migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Database reset complete. You can now create a superuser:"
echo "python manage.py createsuperuser"
