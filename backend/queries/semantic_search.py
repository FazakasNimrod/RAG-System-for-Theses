from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

# Connect to Elasticsearch with authentication
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

model = SentenceTransformer('all-MiniLM-L6-v2')

# Query to search semantically
query_text = "Smart home"
query_embedding = model.encode(query_text)

# Perform a semantic search using script_score for cosine similarity
response = es.search(
    index="theses_with_embeddings",
    query={
        "script_score": {
            "query": {"match_all": {}},  # Retrieve all documents for scoring
            "script": {
                "source": """
                cosineSimilarity(params.query_vector, 'embedding') + 1.0
                """,
                "params": {"query_vector": query_embedding.tolist()}
            }
        }
    },
    size=3  # Limit to top 5 results
)

# Display results
print("Semantic Search Results:\n")
for hit in response['hits']['hits']:
    print(f"Score: {hit['_score']}")
    print(f"Author: {hit['_source']['author']}")
    print(f"Abstract: {hit['_source']['abstract']}")
    print("-" * 50)
