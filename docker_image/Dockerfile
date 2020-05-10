FROM python:3.7

RUN apt-get install -y \
    git

RUN git clone https://jalllychun:compgliCit5y@github.com/Lysarthas/CCCa2.git \
    && cd /CCCa2 \
    && git checkout couchdb_store
RUN pip install -r /CCCa2/crawler/requirements.txt

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
