#!/bin/sh

./wait-for-it.sh db:5432

# Create and seed the database
echo "Creating database tables..."
flask seed-db
echo "Database tables created"

# Create the database migration
echo "Creating database migration..."
flask db init
flask db migrate
flask db upgrade
echo "Database migration created"

exec "$@"