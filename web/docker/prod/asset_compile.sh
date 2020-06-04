#!/bin/sh
python3 /web/manage.py compilescss
python3 /web/manage.py collectstatic --no-input --ignore=*.sass
python3 /web/manage.py compilescss --delete-files
