#!/bin/sh

EXPOSE_PORT=8000

until pg_isready -h db; do
  >&2 echo "postgres is unavailable - sleeping"
  sleep 3
done

python3 /web/manage.py runserver 0.0.0.0:${EXPOSE_PORT}
