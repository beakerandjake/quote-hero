FROM python:3.12.3-slim-bookworm

RUN apt-get update && apt-get install -y curl wget

WORKDIR /ingest

COPY ingest.sh format_bulk_data.py index_settings.json wikiquote_raw.json.gz .

ENTRYPOINT ["./ingest.sh"]