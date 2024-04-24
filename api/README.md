# api

API which serves data to the frontend.

Built with `FastApi`.

## Routes

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
curl localhost:3000/words
```

**NOTE**: The api runs in its own container and is exposed to the host machine on port 3000. It also listens on the internal docker compose network on port 80. The frontend application queries the API via the `reverse-proxy` service which is exposed at `localhost:8080` (by default).

## Local Development

If developing locally, the API can be started by running the following command:

```
uvicorn src.main:app --reload
```

## Build Process

The Dockerfile runs the `bin/load_words_file.sh` script as part of the build. This file attempts to download the words file from `https://github.com/first20hours/google-10000-english`. If for some reason the file fails to download, the system words file will be used as a backup.
