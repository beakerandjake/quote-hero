import logging
import os
import json
import requests
import shutil
import gzip
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "DEBUG").upper(),
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKS_DIR = os.path.join(ROOT_DIR, "chunks")
SUCCESS_DIR = os.path.join(ROOT_DIR, os.environ.get("SUCCESS_FILE_DIR", "success"))
DUMP_FILE_PATH = os.path.join(ROOT_DIR, "wikiquote.json")
ELASTIC_INDEX_CONFIG_PATH = os.path.join(ROOT_DIR, "index_settings.json")

ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "wikiquote")
ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "http://localhost:9200")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/{ELASTIC_INDEX}"

WIKIQUOTE_DUMP_DATE_OVERRIDE = os.environ.get("WIKIQUOTE_DUMP_DATE_OVERRIDE")
WIKIQUOTE_DUMP_ROOT_URL = os.environ.get(
    "WIKIQUOTE_DUMP_ROOT_URL",
    "https://dumps.wikimedia.org/other/cirrussearch/",
)
WIKIQUOTE_DUMP_FILENAME_REGEXP = re.compile(
    os.environ.get(
        "WIKIQUOTE_DUMP_FILENAME_REGEXP",
        r"enwikiquote-[\d]{8}-cirrussearch-content.json.gz",
    )
)


class WikiquoteDumpInfo:
    def __init__(self, date: str, url: str):
        self.date = date
        self.url = url

    def __str__(self):
        return f"Date: {self.date}, Url: {self.url}"


def _get_most_recent_dump_dates() -> list[str]:
    """Returns a list of the most recent wikiquote dump dates"""
    # query the dump root url, this is a directory index and has a list of links to recent dumps.
    index = requests.get(WIKIQUOTE_DUMP_ROOT_URL)
    index.raise_for_status()
    index_soup = BeautifulSoup(index.text, "html.parser")
    # get all links in the directory index (expected links are in asc order, reverse so most recent links are first)
    links = [l.get("href") for l in reversed(index_soup.body.find_all("a"))]
    # match each date link and return the date value.
    date_regexp = re.compile(r"^([0-9]{8})/$")
    return [m.group(1) for m in (date_regexp.match(link) for link in links) if m]


def _find_valid_wikiquote_dump(dates: list[str]) -> WikiquoteDumpInfo:
    """Returns the first date which contains a wikiquote dump"""
    for date in dates:
        # get the directory index of the dump for this date
        dump_url = urljoin(WIKIQUOTE_DUMP_ROOT_URL, f"{date}/")
        r = requests.get(dump_url)
        if r.status_code != 200:
            logger.warn(f"Failed to load dump at date: {date}")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        # get all the links in the directory index
        links = [l.get("href") for l in soup.body.find_all("a")]
        # try to find the wikiquote dump file (it may not have been generated in this dump)
        dump_file = next(
            (link for link in links if WIKIQUOTE_DUMP_FILENAME_REGEXP.match(link)),
            None,
        )
        if dump_file:
            return WikiquoteDumpInfo(date, urljoin(dump_url, dump_file))
    # couldn't find a wikiquote dump in any of the dates.
    return None


def get_dump_date() -> WikiquoteDumpInfo:
    """Returns the date of the wikiquote dump to load"""
    # allow manual override
    if WIKIQUOTE_DUMP_DATE_OVERRIDE is not None:
        logger.debug(
            f"Dump date override is set, using date: {WIKIQUOTE_DUMP_DATE_OVERRIDE}"
        )
        return WIKIQUOTE_DUMP_DATE_OVERRIDE
    logging.info("Finding date of last good wikiquote dump.")
    dates = _get_most_recent_dump_dates()
    if not dates:
        raise RuntimeError("Could not find recent dumps from the wikiquote dump index!")
    return _find_valid_wikiquote_dump(dates)


# def already_ingested(dump_date):
#     """Returns true if this has already ingested the dump for the date"""
#     success_file_path = os.path.join(SUCCESS_DIR, f"success_{dump_date}")
#     logger.info(f"Checking if already imported dump: {success_file_path}")
#     return os.path.isfile(success_file_path)


# def elastic_server_running():
#     """Returns true if the elastic server is running."""
#     logging.debug(f"Checking if elastic server is running at: {ELASTIC_SERVER_URL}")
#     try:
#         r = requests.get(ELASTIC_SERVER_URL)
#         return r.status_code == 200
#     except Exception as e:
#         logger.error(e)
#         return False


# def download_wikiquote_dump(dump_date):
#     """Downloads the elastic search data for wikiquote"""
#     if os.path.isfile(DUMP_FILE_PATH):
#         logging.info(f"Skipping wikiquote dump download, file already exists.")
#         return
#     logging.info(f"Downloading wikiquote dump file.")
#     url = str.format(DUMP_URL_TEMPLATE, date=dump_date)
#     archive_file_path = f"{DUMP_FILE_PATH}.gz"
#     # download the archive
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         # stream file to disk
#         with open(archive_file_path, "wb") as f:
#             for chunk in r.iter_content(2048):
#                 if chunk:
#                     f.write(chunk)
#     # unzip the archive
#     logging.info(f"Decompressing wikiquote dump file.")
#     with gzip.open(archive_file_path, "rb") as src:
#         with open(DUMP_FILE_PATH, "wb") as dest:
#             shutil.copyfileobj(src, dest)
#     # delete the original archive
#     os.remove(archive_file_path)


# def _get_document_keys():
#     """Returns the set of keys to load from each document."""
#     # use the index settings to determine which keys to load.
#     with open(ELASTIC_INDEX_SETTINGS_PATH) as settings:
#         document_keys = set(json.load(settings)["mappings"]["properties"].keys())
#         if not document_keys:
#             raise RuntimeError(
#                 f"Could not load properties from index settings: {ELASTIC_INDEX_SETTINGS_PATH}"
#             )
#         logger.debug(f"Extracting keys: {list(document_keys)} from data dump")
#         return document_keys


# def split_dump_file():
#     """Splits the wikiquote dump file into chunks"""
#     if os.path.isdir("chunks"):
#         logger.info("Skipping dump file chunking, chunk directory already exists.")
#         return
#     logger.info("Splitting dump file into chunks")
#     lines_per_chunk = 500
#     num_chunks = 1
#     current_chunk_file = None
#     document_keys = _get_document_keys()
#     # ensure chunks dir exists before attempt to write to it.
#     os.mkdir(CHUNKS_DIR)
#     with open(DUMP_FILE_PATH) as dump_file:
#         line_num = 0
#         # read every two lines from the file
#         while True:
#             raw_metadata = dump_file.readline()
#             raw_data = dump_file.readline()
#             # eof
#             if not raw_metadata or not raw_data:
#                 break
#             # attempt to write out current chunk file and start a new one.
#             if line_num % lines_per_chunk == 0:
#                 # finish with current chunk file.
#                 if current_chunk_file:
#                     num_chunks += 1
#                     current_chunk_file.close()
#                 # start new chunk file.
#                 new_chunk_file_path = os.path.join(CHUNKS_DIR, f"chunk_{num_chunks}")
#                 current_chunk_file = open(new_chunk_file_path, "w")
#             # write out the metadata and data lines to the chunk file
#             try:
#                 # generate the metadata line and write to the current chunk file
#                 metadata = json.dumps(
#                     {"index": {"_id": json.loads(raw_metadata)["index"]["_id"]}}
#                 )
#                 current_chunk_file.write(metadata + "\n")
#                 # generate the data line and write to the current chunk file
#                 data_json = json.loads(raw_data)
#                 data = json.dumps({key: data_json[key] for key in document_keys})
#                 current_chunk_file.write(data + "\n")
#             except KeyError:
#                 logger.warn(f"Failed to parse document at line: {line_num}")
#             line_num += 2
#     # ensure final chunk in progress in closed
#     if current_chunk_file:
#         current_chunk_file.close()
#     logger.info(f"Split dump file into {num_chunks} chunk file(s).")


# def create_index():
#     """Creates the elastic index to hold the wikiquote data."""
#     # skip creation if index already exists.
#     exists = requests.get(ELASTIC_INDEX_URL)
#     if exists.status_code == 200:
#         logger.info(
#             f"Skipping index creation, index: '{ELASTIC_INDEX}' already exists."
#         )
#         return
#     # create the index with the specified settings
#     logger.info(f"Creating index: '{ELASTIC_INDEX}'")
#     with open(ELASTIC_INDEX_SETTINGS_PATH, "rb") as settings_data:
#         create = requests.put(
#             ELASTIC_INDEX_URL,
#             data=settings_data,
#             headers={"Content-Type": "application/json"},
#         )
#         create.raise_for_status()
#     logger.info(f"Successfully created index: '{ELASTIC_INDEX}'")


# def bulk_load_into_elastic():
#     """Bulk load each chunk into elastic"""
#     logger.info(f"Bulk importing data into index: {ELASTIC_INDEX}.")
#     # post each chunk to the bulk import api
#     for chunk in os.listdir(CHUNKS_DIR):
#         logger.debug(f"importing chunk: {chunk}")
#         with open(os.path.join(CHUNKS_DIR, chunk), "rb") as chunk_data:
#             r = requests.post(
#                 f"{ELASTIC_INDEX_URL}/_bulk",
#                 data=chunk_data,
#                 headers={"Content-Type": "application/x-ndjson"},
#             )
#             if r.status_code != 200:
#                 print(r.content)
#             r.raise_for_status()
#     logger.info("Bulk import success, flushing index.")
#     # ask elastic to flush the index once bulk load is complete
#     requests.post(f"{ELASTIC_INDEX_URL}/_flush")


# def save_success(dump_date):
#     """Writes a success file so the ingest won't occur again for this date"""
#     success_file_path = os.path.join(SUCCESS_DIR, f"success_{dump_date}")
#     logger.debug(f"Saving success file: {success_file_path}")
#     os.makedirs(os.path.dirname(success_file_path), exist_ok=True)
#     open(success_file_path, "w").close()


# def remove_dump_files():
#     """Removes the dump file and chunks from the file system"""
#     logger.info("Removing dump file and chunks")
#     os.remove(DUMP_FILE_PATH)
#     shutil.rmtree(CHUNKS_DIR)


# check if success file exits, if so exit early
def main():
    dump_date = get_dump_date()
    logging.info(f"Starting ingest for date: {dump_date}")
    # # don't re-ingest if already ingested
    # if already_ingested(dump_date):
    #     logging.info(f"Successfully ingested data for dump date: {dump_date}")
    #     return
    # # can't ingest data if the server isn't running
    # if not elastic_server_running():
    #     logging.error("Failed to connect to elasticsearch server")
    #     exit(1)
    # download_wikiquote_dump(dump_date)
    # split_dump_file()
    # create_index()
    # bulk_load_into_elastic()
    # remove_dump_files()
    # save_success(dump_date)
    # logger.info(f"Successfully ingested data for date: {dump_date}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
        exit(1)
