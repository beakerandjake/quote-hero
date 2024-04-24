import logging
import os
import requests
import shutil
import gzip
import re
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

WIKIQUOTE_DUMP_DATE_OVERRIDE = os.environ.get("WIKIQUOTE_DUMP_DATE_OVERRIDE")
WIKIQUOTE_DUMP_ROOT_URL = os.environ.get(
    "WIKIQUOTE_DUMP_ROOT_URL",
    "https://dumps.wikimedia.org/other/cirrussearch/",
)


class WikiquoteDumpInfo:
    """Contains information about a wikiquote dump"""

    def __init__(self, date: str, url: str):
        self.date = date
        self.url = url

    def __str__(self):
        return f"Date: {self.date}, Url: {self.url}"


def _get_most_recent_dump_dates() -> list[str]:
    """Returns a list of the most recent wikiquote dump dates"""
    logger.debug("Grabbing list of most recent wikimedia dumps.")
    # query the dump root url, this is a directory index and has a list of links to recent dumps.
    index = requests.get(WIKIQUOTE_DUMP_ROOT_URL)
    index.raise_for_status()
    index_soup = BeautifulSoup(index.text, "html.parser")
    # get all links in the directory index (expected links are in asc order, reverse so most recent links are first)
    links = [l.get("href") for l in reversed(index_soup.body.find_all("a"))]
    # match each date link and return the date value.
    date_regexp = re.compile(r"^([0-9]{8})/$")
    return [m.group(1) for m in (date_regexp.match(link) for link in links) if m]


def _file_name(date: str) -> str:
    """Returns the expected name of the wikiquote dump file for the specified date"""
    return f"enwikiquote-{date}-cirrussearch-content.json.gz"


def _url_for_date(date: str) -> str:
    """Returns a url to the directory index of the dump at the specified date"""
    return urljoin(WIKIQUOTE_DUMP_ROOT_URL, f"{date}/")


def _file_url(date: str) -> str:
    """Returns the url to a wikiquote dump file for the specified date"""
    return urljoin(_url_for_date(date), _file_name(date))


def _first_valid_wikiquote_dump(dates: list[str]) -> Optional[WikiquoteDumpInfo]:
    """Returns info for the first date which contains a wikiquote dump (if any)"""
    for date in dates:
        logger.debug(f"Searching dump: {date} for a wikiquote dump.")
        # get the directory index of the dump for this date
        index = requests.get(_url_for_date(date))
        if index.status_code != 200:
            logger.warn(f"Failed to load dump at date: {date}")
            continue
        soup = BeautifulSoup(index.text, "html.parser")
        # get all the links in the directory index
        links = [l.get("href") for l in soup.body.find_all("a")]
        # see if this date has the file we need
        dump_file_name = _file_name(date)
        if next((l for l in links if l == dump_file_name), None):
            return WikiquoteDumpInfo(date, _file_url(date))
    # couldn't find a wikiquote dump in any of the dates.
    return None


def get_latest_dump_info() -> Optional[WikiquoteDumpInfo]:
    """Returns the info of the most recent wikiquote dump"""
    # allow manual override
    if WIKIQUOTE_DUMP_DATE_OVERRIDE is not None:
        logger.debug(
            f"Dump date override is set, using date: {WIKIQUOTE_DUMP_DATE_OVERRIDE}"
        )
        return WikiquoteDumpInfo(
            WIKIQUOTE_DUMP_DATE_OVERRIDE, _file_url(WIKIQUOTE_DUMP_DATE_OVERRIDE)
        )
    logging.info("Finding date of last good wikiquote dump.")
    return _first_valid_wikiquote_dump(_get_most_recent_dump_dates())


def download(dump_info: WikiquoteDumpInfo, dest: str):
    """Downloads the elastic search data for wikiquote"""
    if os.path.isfile(dest):
        logging.info(f"Skipping wikiquote dump download, file already exists.")
        return
    archive_file = _file_name(dump_info.date)
    logging.info("Downloading wikiquote dump archive.")
    # download the archive
    with requests.get(dump_info.url, stream=True) as r:
        r.raise_for_status()
        # stream file to disk.
        with open(archive_file, "wb") as f:
            for chunk in r.iter_content(2048):
                if chunk:
                    f.write(chunk)
    # unzip the archive
    logging.debug(f"Unpacking dump file archive: '{archive_file}'.")
    with gzip.open(archive_file, "rb") as src:
        with open(dest, "wb") as dest:
            shutil.copyfileobj(src, dest)
    # delete the original archive
    logging.debug(f"Deleting archive file.")
    os.remove(archive_file)
