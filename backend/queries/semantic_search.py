from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

model = SentenceTransformer('all-MiniLM-L6-v2')

query_text = "Smart home"
query_embedding = model.encode(query_text)

response = es.search(
    index="theses_with_embeddings",
    query={
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": """
                cosineSimilarity(params.query_vector, 'embedding') + 1.0
                """,
                "params": {"query_vector": query_embedding.tolist()}
            }
        }
    },
    size=3 
)

print("Semantic Search Results:\n")
for hit in response['hits']['hits']:
    print(f"Score: {hit['_score']}")
    print(f"Author: {hit['_source']['author']}")
    print(f"Abstract: {hit['_source']['abstract']}")
    print("-" * 50)
