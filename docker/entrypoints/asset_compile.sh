#!/bin/sh
python3 manage.py compilescss
python3 manage.py collectstatic --no-input --ignore=*.sass --settings=config.environments.production
# python3 /web/manage.py compilescss --delete-files
