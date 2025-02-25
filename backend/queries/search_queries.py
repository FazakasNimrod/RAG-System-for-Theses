from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

search_query = {
    "query": {
        "match": {
            "abstract": "smart home"
        }
    }
}

response = es.search(index="theses", body=search_query)

for hit in response['hits']['hits']:
    doc_id = hit['_id']
    source = hit['_source']
    print(f"Document ID: {doc_id}")
    print(f"Document Content: {source}\n")
