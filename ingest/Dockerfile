FROM python:3.12.3

WORKDIR /ingest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingest.py index_settings.json wikiquote.json .

CMD [ "python", "./ingest.py" ]