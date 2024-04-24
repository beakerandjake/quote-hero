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
SUCCESS_DIR = os.path.join(ROOT_DIR, "success")
LOCAL_DUMP_FILE_PATH = os.path.join(ROOT_DIR, "wikiquote.json")
ELASTIC_INDEX_CONFIG_PATH = os.path.join(ROOT_DIR, "index_settings.json")


def _already_ingested(date: str) -> bool:
    """Returns true if this has already ingested the dump for the date"""
    success_file_path = os.path.join(SUCCESS_DIR, f"success_{date}")
    logger.info(f"Checking if already imported dump for date: {date}")
    return os.path.isfile(success_file_path)


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


def _save_ingest_success(date: str):
    """Writes a success file so the ingest won't occur again for this date"""
    success_file_path = os.path.join(SUCCESS_DIR, f"success_{date}")
    logger.debug(f"Saving ingest success: {success_file_path}")
    os.makedirs(os.path.dirname(success_file_path), exist_ok=True)
    open(success_file_path, "w").close()


# check if success file exits, if so exit early
def main():
    logging.debug("Starting ingest.")
    dump_info = wikiquote.get_latest_dump_info()
    logging.info(f"Starting ingest for date: {dump_info}")
    # don't re-ingest if already ingested
    if _already_ingested(dump_info.date):
        logging.info(f"Successfully ingested data for dump date: {dump_info.date}")
        return
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
    _save_ingest_success(dump_info.date)
    logger.info(f"Successfully ingested data for date: {dump_info.date}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
        exit(1)
