from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch

# Load environment variables from .env
load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

# Connect to Elasticsearch with authentication
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

# Query to fetch all documents from the 'theses_with_embeddings' index
response = es.search(index="theses_with_embeddings", query={"match_all": {}}, size=1000)  # Fetch up to 1000 documents

# Display the results
if "hits" in response and "hits" in response["hits"]:
    print("Index: theses_with_embeddings\n")
    for hit in response["hits"]["hits"]:
        print(hit["_source"])  # Display the source of each document
        print()
else:
    print("No documents found in the index.")