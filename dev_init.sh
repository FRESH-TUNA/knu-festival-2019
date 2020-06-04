#!/bin/sh

# volume 초기화
#rm -rf db/volume

# development image build
echo "1. development image build"
docker-compose build

# migrate
echo "2. db migrate"
docker-compose up -d db
docker-compose run --entrypoint="sh ./docker/init.sh" web

# finish
docker-compose down
echo "development environment finished!"
