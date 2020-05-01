#!/bin/sh

# until wget db:5432  -O /dev/null; do
#   >&2 echo "mysql is unavailable - sleeping"
#   sleep 3
# done

python3 /web/manage.py makemigrations
python3 /web/manage.py migrate