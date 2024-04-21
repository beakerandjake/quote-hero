import os
from elasticsearch import Elasticsearch

ELASTIC_SERVER_URL = os.environ.get("ELASTIC_SERVER_URL", "http://localhost:9200")
ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", "wikiquote")
ELASTIC_INDEX_URL = f"{ELASTIC_SERVER_URL}/{ELASTIC_INDEX}"
client = Elasticsearch(ELASTIC_SERVER_URL)


def test_query():
    return client.get(index=ELASTIC_INDEX, id=99998)
