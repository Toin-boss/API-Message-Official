FROM postgres:17 

RUN apt-get update \
    && apt-get install -y \
        postgresql-17-postgis-3 \
        postgresql-17-postgis-3-scripts \
    && rm -rf /var/lib/apt/list/*