#!/bin/sh

until pg_isready -h db; do
  >&2 echo "postgres is unavailable - sleeping"
  sleep 3
done

python3 /web/manage.py makemigrations
python3 /web/manage.py migrate