#!/bin/sh

# migrate
docker-compose run --entrypoint="sh ./docker/prod/asset_compile.sh" web
cp -r ../web/static ./
rm -rf ../web/static

# finish
docker build -t lunacircle4/knufestival2019-nginx:latest .
rm -rf ./static
