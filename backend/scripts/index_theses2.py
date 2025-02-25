from dotenv import load_dotenv
import os
import json
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

with open("theses_with_embeddings.json", "r") as f:
    theses_data = json.load(f)

for thesis in theses_data:
    es.index(index="theses_with_embeddings", document=thesis)

print("Data indexed successfully.")
