#!/bin/sh

echo "wait for postgres"

until pg_isready -h db; do
  >&2 echo "."
  sleep 3
done

supervisord
