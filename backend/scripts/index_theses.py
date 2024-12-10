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
with open("theses.json", "r") as f:
    theses_data = json.load(f)

# Index each document with an explicit ID
for i, thesis in enumerate(theses_data, start=1):
    es.index(index="theses", id=i, document=thesis)

print("Data indexed successfully with explicit IDs.")
