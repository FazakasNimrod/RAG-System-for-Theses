from dotenv import load_dotenv
import os
import json
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Connect to Elasticsearch with authentication
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=("elastic", ELASTIC_PASSWORD)  # Add your credentials here
)

# Load the theses data from the JSON file
with open("theses_with_embeddings.json", "r") as f:
    theses_data = json.load(f)

# Index each document
for thesis in theses_data:
    es.index(index="theses_with_embeddings", document=thesis)

print("Data indexed successfully.")
