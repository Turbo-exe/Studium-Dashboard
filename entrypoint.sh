#!/bin/sh

# Wait for a moment to ensure everything is ready
sleep 2

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Check if the database needs to be prefilled
echo "Checking if database needs to be prefilled..."
python manage.py prefill_database

# Start the main application
echo "Starting the application..."
exec "$@"
