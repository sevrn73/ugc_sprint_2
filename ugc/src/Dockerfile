FROM python:3.9-alpine

WORKDIR /opt/ugc_api

COPY requirements.txt requirements.txt
RUN  apk update && \
     apk add build-base librdkafka-dev && \
     apk --no-cache add curl && \
     pip install --upgrade pip && \
     pip install -r requirements.txt --no-cache-dir

COPY . .

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
