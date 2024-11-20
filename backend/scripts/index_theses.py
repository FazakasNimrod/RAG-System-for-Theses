import json
from elasticsearch import Elasticsearch

# Connect to Elasticsearch with authentication
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=("elastic", "erBWhWE2*9HFerd2Az10")  # Add your credentials here
)

# Load the theses data from the JSON file
with open("theses.json", "r") as f:
    theses_data = json.load(f)

# Index each document
for thesis in theses_data:
    es.index(index="theses", document=thesis)

print("Data indexed successfully.")
