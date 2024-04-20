import logging
import os
import json
import requests
import shutil
import gzip

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "DEBUG").upper(),
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SUCCESS_FILE_DIR = os.path.join(ROOT_DIR, os.environ.get("SUCCESS_FILE_DIR", "success"))
ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "wikiquote")
ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "http://localhost:9200")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/{ELASTIC_INDEX}"
ELASTIC_INDEX_SETTINGS_PATH = os.path.join(ROOT_DIR, "index_settings.json")
DUMP_DATE = os.environ.get("DUMP_DATE", "20240415")
DUMP_URL_TEMPLATE = os.environ.get(
    "DUMP_URL_TEMPLATE",
    # "https://dumps.wikimedia.org/other/cirrussearch/{date}/etwikimedia-{date}-cirrussearch-general.json.gz",
    "https://dumps.wikimedia.org/other/cirrussearch/{date}/enwikiquote-{date}-cirrussearch-content.json.gz",
)
DUMP_FILE_PATH = os.path.join(ROOT_DIR, "wikiquote.json")
CHUNKS_DIR = os.path.join(ROOT_DIR, "chunks")


def get_dump_date():
    """Returns the date of the wikiquote dump to load"""
    # todo, if not set, search and use last good backup from wikimedia.
    logging.info("Loading dump date...")
    return DUMP_DATE


def already_ingested(dump_date):
    """Returns true if this has already ingested the dump for the date"""
    success_file_path = os.path.join(SUCCESS_FILE_DIR, f"success_{dump_date}")
    logger.info(f"Checking if already imported dump: {success_file_path}")
    return os.path.isfile(success_file_path)


def elastic_server_running():
    """Returns true if the elastic server is running."""
    logging.debug(f"Checking if elastic server is running at: {ELASTIC_SERVER_URL}")
    try:
        r = requests.get(ELASTIC_SERVER_URL)
        return r.status_code == 200
    except Exception as e:
        logger.error(e)
        return False


def download_wikiquote_dump(dump_date):
    """Downloads the elastic search data for wikiquote"""
    if os.path.isfile(DUMP_FILE_PATH):
        logging.info(f"Skipping wikiquote dump download, file already exists.")
        return
    logging.info(f"Downloading wikiquote dump file.")
    url = str.format(DUMP_URL_TEMPLATE, date=dump_date)
    archive_file_path = f"{DUMP_FILE_PATH}.gz"
    # download the archive
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        # stream file to disk
        with open(archive_file_path, "wb") as f:
            for chunk in r.iter_content(2048):
                if chunk:
                    f.write(chunk)
    # unzip the archive
    logging.info(f"Decompressing wikiquote dump file.")
    with gzip.open(archive_file_path, "rb") as src:
        with open(DUMP_FILE_PATH, "wb") as dest:
            shutil.copyfileobj(src, dest)
    # delete the original archive
    os.remove(archive_file_path)


def split_dump_file():
    """Splits the wikiquote dump file into chunks"""
    if os.path.isdir("chunks"):
        logger.info("Skipping dump file chunking, chunk directory already exists.")
        return
    logger.info("Splitting dump file into chunks")
    lines_per_chunk = 500
    num_chunks = 1
    current_chunk_file = None
    document_keys = {}
    # load the keys specified by the index settings.
    with open(ELASTIC_INDEX_SETTINGS_PATH) as settings:
        document_keys = set(json.load(settings)["mappings"]["properties"].keys())
        if not document_keys:
            raise RuntimeError(
                f"Could not load properties from index settings: {ELASTIC_INDEX_SETTINGS_PATH}"
            )
        logger.debug(f"Extracting keys: {list(document_keys)} from data dump")
    # ensure chunks dir exists before attempt to write to it.
    os.mkdir(CHUNKS_DIR)
    with open(DUMP_FILE_PATH) as dump_file:
        for i, line in enumerate(dump_file):
            # write out current chunk file and start a new one.
            if i % lines_per_chunk == 0:
                if current_chunk_file:
                    num_chunks += 1
                    current_chunk_file.close()
                new_chunk_file_path = os.path.join(CHUNKS_DIR, f"chunk_{num_chunks}")
                current_chunk_file = open(new_chunk_file_path, "w")
            formatted = None
            # expect even lines are for metadata
            if i % 2 == 0:
                formatted = json.dumps(
                    {"index": {"_id": json.loads(line)["index"]["_id"]}}
                )
            # expect odd lines are for documents
            else:
                line_json = json.loads(line)
                formatted = json.dumps(
                    {key: line_json.get(key) for key in document_keys}
                )
            # write the formatted line to the current chunk file
            current_chunk_file.write(formatted + "\n")
    # ensure final chunk in progress in closed
    if current_chunk_file:
        current_chunk_file.close()
    logger.info(f"Split dump file into {num_chunks} chunk file(s).")


def create_index():
    """Creates the elastic index to hold the wikiquote data."""
    # skip creation if index already exists.
    exists = requests.get(ELASTIC_INDEX_URL)
    if exists.status_code == 200:
        logger.info(
            f"Skipping index creation, index: '{ELASTIC_INDEX}' already exists."
        )
        return
    # create the index with the specified settings
    logger.info(f"Creating index: '{ELASTIC_INDEX}'")
    with open(ELASTIC_INDEX_SETTINGS_PATH, "rb") as settings_data:
        create = requests.put(
            ELASTIC_INDEX_URL,
            data=settings_data,
            headers={"Content-Type": "application/json"},
        )
        create.raise_for_status()
    logger.info(f"Successfully created index: '{ELASTIC_INDEX}'")


def bulk_load_into_elastic():
    """Bulk load each chunk into elastic"""
    logger.info(f"Bulk importing data into index: {ELASTIC_INDEX}.")
    # post each chunk to the bulk import api
    for chunk in os.listdir(CHUNKS_DIR):
        logger.debug(f"importing chunk: {chunk}")
        with open(os.path.join(CHUNKS_DIR, chunk), "rb") as chunk_data:
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


def save_success(dump_date):
    """Writes a success file so the ingest won't occur again for this date"""
    success_file_path = os.path.join(SUCCESS_FILE_DIR, f"success_{dump_date}")
    logger.debug(f"Saving success file: {success_file_path}")
    os.makedirs(os.path.dirname(success_file_path), exist_ok=True)
    open(success_file_path, "w").close()


def remove_dump_files():
    """Removes the dump file and chunks from the file system"""
    logger.info("Removing dump file and chunks")
    os.remove(DUMP_FILE_PATH)
    shutil.rmtree(CHUNKS_DIR)


# check if success file exits, if so exit early
def main():
    dump_date = get_dump_date()
    logging.info(f"Starting ingest for date: {dump_date}")
    # don't re-ingest if already ingested
    if already_ingested(dump_date):
        logging.info(f"Successfully ingested data for dump date: {dump_date}")
        return
    # can't ingest data if the server isn't running
    if not elastic_server_running():
        logging.error("Failed to connect to elasticsearch server")
        exit(1)
    download_wikiquote_dump(dump_date)
    split_dump_file()
    create_index()
    bulk_load_into_elastic()
    remove_dump_files()
    save_success(dump_date)
    logger.info(f"Successfully ingested data for date: {dump_date}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
        exit(1)
