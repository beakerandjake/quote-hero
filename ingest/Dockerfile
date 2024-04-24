FROM python:3.12.3

WORKDIR /ingest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY index_settings.json .
COPY src src

CMD [ "python", "src/main.py" ]