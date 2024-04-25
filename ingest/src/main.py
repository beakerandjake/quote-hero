import logging
import os
import json
import shutil
import wikiquote
import chunks
import elastic

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "DEBUG").upper(),
)

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
CHUNKS_DIR = os.path.join(ROOT_DIR, "chunks")
SUCCESS_FILE_PATH = os.path.join(ROOT_DIR, 'success', 'success.log')
LOCAL_DUMP_FILE_PATH = os.path.join(ROOT_DIR, "wikiquote.json")
ELASTIC_INDEX_CONFIG_PATH = os.path.join(ROOT_DIR, "index_settings.json")


def _already_ingested() -> bool:
    """Returns true if the success file exists, indicating that the ingest process has already ran."""
    logger.info(f"Checking if ingest has already ran.")
    return os.path.isfile(SUCCESS_FILE_PATH)


def _get_index_keys() -> dict:
    """Returns the set of keys to load from each document in the dump."""
    # use the index settings to determine which keys to load.
    with open(ELASTIC_INDEX_CONFIG_PATH) as settings:
        document_keys = set(json.load(settings)["mappings"]["properties"].keys())
        if not document_keys:
            raise RuntimeError(
                f"Could not load properties from index settings: {ELASTIC_INDEX_CONFIG_PATH}"
            )
        logger.debug(f"Extracting index keys: {list(document_keys)} from dump.")
        return document_keys


def _clean_up_files():
    """Removes the dump file and chunks from the file system"""
    logger.info("Removing dump file and chunks.")
    os.remove(LOCAL_DUMP_FILE_PATH)
    shutil.rmtree(CHUNKS_DIR)


def _save_ingest_success():
    """Writes a success file so the ingest won't occur again."""
    logger.debug(f"Saving ingest success file to: {SUCCESS_FILE_PATH}")
    os.makedirs(os.path.dirname(SUCCESS_FILE_PATH), exist_ok=True)
    open(SUCCESS_FILE_PATH, "w").close()


# check if success file exits, if so exit early
def main():
    logging.debug("Starting ingest.")
    # don't re-ingest if already ingested
    if _already_ingested():
        logging.info(f"Ingest process already completed.")
        return
    dump_info = wikiquote.get_latest_dump_info()
    logging.info(f"Starting ingest for date: {dump_info}")
    # can't ingest data if the server isn't running
    if not elastic.server_running():
        logging.error("Failed to connect to elasticsearch server")
        exit(1)
    # download the dump file, split it into chunks, and bulk load the chunks into elastic.
    wikiquote.download(dump_info, LOCAL_DUMP_FILE_PATH)
    chunks.chunk_dump_file(LOCAL_DUMP_FILE_PATH, CHUNKS_DIR, _get_index_keys())
    elastic.create_index(ELASTIC_INDEX_CONFIG_PATH)
    elastic.bulk_load(CHUNKS_DIR)
    _clean_up_files()
    _save_ingest_success()
    logger.info(f"Successfully ingested data for date: {dump_info.date}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
        exit(1)
