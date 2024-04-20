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
ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "https://localhost:9200")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/wikiquote"
DUMP_FILE_PATH = "wikiquote.json"
CHUNKS_DIR = "chunks"
WIKI_DUMP_URL_TEMPLATE = os.environ.get(
    "WIKIQUOTE_DUMP_URL_TEMPLATE",
    "https://dumps.wikimedia.org/other/cirrussearch/{date}/etwikimedia-{date}-cirrussearch-general.json.gz",
    # "https://dumps.wikimedia.org/other/cirrussearch/{date}/enwikiquote-{date}-cirrussearch-content.json.gz",
)


def get_dump_date():
    """Returns the date of the wikiquote dump to load"""
    # todo, use env variable or if not set find last good backup from wikimedia.
    logging.info("Loading dump date...")
    return os.environ.get("DUMP_DATE", "20240415")


def ensure_server_running():
    """Returns true if the elastic server is running."""
    logging.debug(f"Checking if elastic server is running at: {ELASTIC_SERVER_URL}")
    try:
        return (
            requests.get(
                ELASTIC_SERVER_URL,
                auth=("elastic", "elastic"),
                verify=False,
            ).status_code
            == 200
        )
    except Exception as e:
        logger.error(e)
        return False


def download_wikiquote_dump(dump_date):
    """Downloads the elastic search data for wikiquote"""
    if os.path.isfile(DUMP_FILE_PATH):
        logging.info(f"Skipping wikiquote dump download, file already exists.")
        return
    logging.info(f"Downloading wikiquote dump file.")
    url = str.format(WIKI_DUMP_URL_TEMPLATE, date=dump_date)
    archive_file_path = "dump.gz"

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
    num_chunks = 0
    current_chunk_file = None
    document_keys = {"title", "page_id", "text"}
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
                formatted = json.dumps({key: line_json[key] for key in document_keys})
            # write the formatted line to the current chunk file
            current_chunk_file.write(formatted + "\n")
    # ensure final chunk in progress in closed
    if current_chunk_file:
        current_chunk_file.close()


# check if success file exits, if so exit early
def main():
    dump_date = get_dump_date()
    logging.info(f"Starting ingest for date: {dump_date}")
    # can't ingest data if the server isn't running
    if not ensure_server_running():
        logging.error("Failed to connect to elasticsearch server")
        exit(1)
    download_wikiquote_dump(dump_date)
    split_dump_file()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
        exit(1)
