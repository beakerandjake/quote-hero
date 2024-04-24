# api

API which serves data to the frontend.

Built with `FastApi`.

## Routes

**NOTE**: When you run this service via docker compose these routes are accessible at `localhost:8080/api`. This is because the service is behind the `reverse-proxy` service. Using the reverse proxy removes the need for cors.

### /docs

The Swagger docs for the API.

### /words

Returns a random word.

### /search

Searches for matching documents which contain the search terms.

### /stats

Returns information about the elasticsearch index.

## Usage

This application depends on the elasticsearch service being healthy, and is intended to be ran through docker compose.

At the root of the repo run:

```sh
docker compose up -d
```

After all the containers have started up you can verify the api is serving data by running:

```sh
curl localhost:8080/api/words
```

## Local Development

If developing locally, the API can be started by running the following command:

```
uvicorn src.main:app --reload
```

## Build Process

The Dockerfile runs the `bin/load_words_file.sh` script as part of the build. This file attempts to download the words file from `https://github.com/first20hours/google-10000-english`. If for some reason the file fails to download, the system words file will be used as a backup.
