#!/bin/bash
# Credit to Michael Herman from testdriven.io

if [ "$DB" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Flush and apply database migrations every time
python manage.py flush --no-input
python manage.py migrate

exec "$@"