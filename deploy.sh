#!/bin/bash

DOCKER_APP_NAME=knufestival

EXIST_BLUE=$(docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.blue.yml ps | grep Up)

docker-compose -p knufestival -f /app/docker-compose/prod/docker-compose.blue.yml ps | grep Up

docker pull lunacircle4/knu-festival

if [ -n "$EXIST_BLUE" ]; then
    echo "green up"
    docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.green.yml up -d
    sleep 10
    GREEN_CONTAINER=$(docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.green.yml ps | grep Up)
    if [ -n "$GREEN_CONTAINER" ]; then
        docker exec knufestival_nginx_1 /bin/bash -c "rm /etc/nginx/conf.d/nginx.blue.conf"
        docker exec knufestival_nginx_1 /bin/bash -c "cp /app/conf/nginx.conf /etc/nginx/conf.d"
        docker exec knufestival_nginx_1 /bin/bash -c "nginx -s reload"

        sleep 10

        docker exec knufestival_nginx_1 /bin/bash -c "rm /etc/nginx/conf.d/nginx.conf"
        docker exec knufestival_nginx_1 /bin/bash -c "cp /app/conf/nginx.green.conf /etc/nginx/conf.d"
        docker exec knufestival_nginx_1 /bin/bash -c "nginx -s reload"
        docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.blue.yml down
    else
        echo "failed"
    fi
else
    echo "blue up"
    docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.blue.yml up -d
    sleep 10
    BLUE_CONTAINER=$(docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.blue.yml ps | grep Up)

    if [ -n "$BLUE_CONTAINER" ]; then
        docker exec knufestival_nginx_1 /bin/bash -c "rm /etc/nginx/conf.d/nginx.green.conf"
        docker exec knufestival_nginx_1 /bin/bash -c "cp /app/conf/nginx.conf /etc/nginx/conf.d"
        docker exec knufestival_nginx_1 /bin/bash -c "nginx -s reload"

        sleep 10

        docker exec knufestival_nginx_1 /bin/bash -c "rm /etc/nginx/conf.d/nginx.conf"
        docker exec knufestival_nginx_1 /bin/bash -c "cp /app/conf/nginx.blue.conf /etc/nginx/conf.d"
        docker exec knufestival_nginx_1 /bin/bash -c "nginx -s reload"
        docker-compose -p ${DOCKER_APP_NAME} -f /app/docker-compose/prod/docker-compose.green.yml down
    else
        echo "failed"
    fi
fi
