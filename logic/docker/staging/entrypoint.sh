#!/bin/sh

echo "wait for postgres"

until pg_isready -h knufestival2019-db-service; do
  >&2 echo "."
  sleep 3
done

supervisord
