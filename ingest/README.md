# ingest

The ingest application is responsible for creating the elasticsearch wikiquote index and populating it with data. Wikimedia conveniently posts [dumps](https://dumps.wikimedia.org/other/cirrussearch/) formatted for elastic search bulk import, which the ingest process uses. It attempts to load the most recent dump of wikiquote automatically.

## Usage

This application depends on the elastic service, and is intended to be ran through docker compose.

At the root of the repo run:

```sh
docker compose up -d
```

## Configuration

- `WIKIQUOTE_DUMP_DATE_OVERRIDE` - Allows you to manually specific a date, expected format is YYYYMMDD.
- `WIKIQUOTE_DUMP_ROOT_URL` - The directory index of the wikimedia elasticsearch dumps.
- `ELASTIC_INDEX` - The name of the index to ingest data into.
- `ELASTIC_SERVER_URL` - The url of the elasticsearch server to ingest data into.
