import os
from elasticsearch import Elasticsearch


ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "http://localhost:9200")
ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "wikiquote")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/{ELASTIC_INDEX}"
client = Elasticsearch(ELASTIC_SERVER_URL)


def num_docs():
    """Returns the total number of documents"""
    return client.count(index=ELASTIC_INDEX)["count"]


def _map_results(results):
    """Extracts the necessary information from the raw elasticsearch results."""
    return {
        "total": results["hits"]["total"]["value"],
        "top": [item["_source"] for item in results["hits"]["hits"]],
    }


def search_exact(terms: list[str]):
    """Returns all documents which match the terms exactly"""
    results = client.search(
        index=ELASTIC_INDEX,
        query={"match_phrase": {"text": {"query": " ".join(terms), "slop": 4}}},
        source=["title", "page_id"],
    )
    return _map_results(results)


def search_fuzzy(terms: list[str]):
    """Returns all documents which contain all of the terms"""
    results = client.search(
        index=ELASTIC_INDEX,
        query={"match": {"text": {"query": " ".join(terms), "operator": "and"}}},
        source=["title", "page_id"],
    )
    return _map_results(results)
