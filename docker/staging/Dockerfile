# production
FROM lunacircle4/python:3.8.1

WORKDIR /logic

RUN apt update \
    && apt install -y postgresql postgresql-contrib libpq-dev supervisor zlib1g-dev libjpeg-dev \         
    && rm -rf /var/lib/apt/lists/* 
s
COPY requirements.txt ./
RUN pip3 --no-cache-dir install -r requirements.txt && rm -rf requirements.txt

COPY . .
RUN cp ./docker/staging/supervisord.was.conf /etc/supervisor/conf.d

ENTRYPOINT ["sh", "./docker/staging/service"]
