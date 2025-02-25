from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

response = es.search(index="theses_with_embeddings", query={"match_all": {}}, size=1000)

if "hits" in response and "hits" in response["hits"]:
    print("Index: theses_with_embeddings\n")
    for hit in response["hits"]["hits"]:
        print(hit["_source"])
        print()
else:
    print("No documents found in the index.")
