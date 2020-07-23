# development
FROM lunacircle4/python:3.8.1
WORKDIR /logic
EXPOSE 8000
COPY requirements.txt ./
RUN apt update \
    && apt install -y postgresql postgresql-contrib libpq-dev supervisor zlib1g-dev libjpeg-dev \        
    && rm -rf /var/lib/apt/lists/*
    
RUN pip3 --no-cache-dir install -r requirements.txt
ENTRYPOINT ["sh", "./docker/development/service"]
