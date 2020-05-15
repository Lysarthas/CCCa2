FROM python:3.7-slim

ADD ./ /code/

RUN pip install --no-cache-dir -r /code/crawler/requirements.txt

COPY ./docker_image/entrypoint.sh entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
