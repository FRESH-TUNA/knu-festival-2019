#!/bin/sh
python3 /web/manage.py compilescss
python3 /web/manage.py collectstatic --no-input --ignore=*.sass --settings=config.environments.production
# python3 /web/manage.py compilescss --delete-files
