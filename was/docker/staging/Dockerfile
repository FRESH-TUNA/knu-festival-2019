# production
FROM lunacircle4/python:3.8.1
WORKDIR /web
COPY . .
RUN apt update \
    && apt install -y postgresql postgresql-contrib libpq-dev supervisor \         
    && rm -rf /var/lib/apt/lists/* \
    && cp ./docker/prod/supervisord_was.conf /etc/supervisor/conf.d
    
RUN pip3 --no-cache-dir install -r requirements.txt
ENTRYPOINT ["sh", "./docker/prod/entrypoint.sh"]
