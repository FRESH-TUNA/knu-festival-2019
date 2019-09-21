#!/bin/zsh

# now using docker cloud 
# docker build -t lunacircle4/knu-festival:1.0.0  -f docker/prod/Dockerfile .
# docker push lunacircle4/knu-festival:1.0.0
# docker tag lunacircle4/knu-festival:1.0.0 lunacircle4/floweryroad-backend:latest
# docker push lunacircle4/knu-festival:latest

# nginx build, now using docker cloud 
# docker build -t lunacircle4/nginx:floweryroad-backend  -f docker/nginx/prod/Dockerfile .
# docker push lunacircle4/nginx:floweryroad-backend

ssh -tt -i <pem경로> ec2-user@http://52.79.154.224/   "\
                                    docker-compose -f /app/docker-compose.yml down  && \
                                    docker-compose -f /app/docker-compose.yml pull  && \
                                    docker-compose -f /app/docker-compose.yml up -d"