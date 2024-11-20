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

# Test the connection
if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Failed to connect.")
