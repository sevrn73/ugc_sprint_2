FROM python:3.9-alpine

WORKDIR /opt/ugc_etl

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && \
     pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT python /opt/ugc_etl/etl_process.py