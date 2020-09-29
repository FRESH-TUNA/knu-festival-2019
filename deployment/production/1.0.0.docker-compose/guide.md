docker build -t lunacircle4/logic.knufesta2019:1.0.0-test -f logic/docker/staging/Dockerfile logic
docker-compose -f deployment/staging/1.0.0/docker-compose.yaml up

docker build -t lunacircle4/logic.knufesta2019:1.0.0 -f logic/docker/production/Dockerfile logic
docker-compose -f deployment/production/1.0.0/docker-compose.yaml up
