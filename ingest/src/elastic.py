import logging
import os
import requests

logger = logging.getLogger(__name__)


ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "wikiquote")
ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "http://localhost:9200")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/{ELASTIC_INDEX}"


def server_running() -> bool:
    """Returns true if the elastic server is running."""
    logging.debug(f"Checking if elastic server is running at: {ELASTIC_SERVER_URL}")
    try:
        return requests.get(ELASTIC_SERVER_URL).status_code == 200
    except Exception as e:
        logger.error(e)
        return False


def create_index(config_path: str):
    """Creates an elastic index to hold the wikiquote data."""
    # skip creation if index already exists.
    exists = requests.get(ELASTIC_INDEX_URL)
    if exists.status_code == 200:
        logger.info(
            f"Skipping index creation, index: '{ELASTIC_INDEX}' already exists."
        )
        return
    # create the index with the specified settings
    logger.info(f"Creating index: '{ELASTIC_INDEX}'")
    with open(config_path, "rb") as config_data:
        create = requests.put(
            ELASTIC_INDEX_URL,
            data=config_data,
            headers={"Content-Type": "application/json"},
        )
        create.raise_for_status()
    logger.info(f"Successfully created index: '{ELASTIC_INDEX}'")


def bulk_load(data_dir: str):
    """Bulk loads all of the files in the directory into the wikiquote index."""
    logger.info(f"Bulk importing data into index: {ELASTIC_INDEX}.")
    # post each chunk to the bulk import api
    for chunk in os.listdir(data_dir):
        logger.debug(f"importing chunk: {chunk}")
        with open(os.path.join(data_dir, chunk), "rb") as chunk_data:
            r = requests.post(
                f"{ELASTIC_INDEX_URL}/_bulk",
                data=chunk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )
            if r.status_code != 200:
                print(r.content)
            r.raise_for_status()
    logger.info("Bulk import success, flushing index.")
    # ask elastic to flush the index once bulk load is complete
    requests.post(f"{ELASTIC_INDEX_URL}/_flush")
