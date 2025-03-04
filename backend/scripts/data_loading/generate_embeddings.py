from dotenv import load_dotenv
import os
import json
import numpy as np
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

"""
This script:
1. Loads your existing JSON data
2. Creates embeddings for each abstract using SentenceTransformer
3. Updates the Elasticsearch mapping to include vector fields
4. Indexes the data with embeddings into a new index
"""

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

if not es.ping():
    print("Failed to connect to Elasticsearch")
    exit(1)
print("Connected to Elasticsearch!")

try:
    with open("backend/scripts/pdf_processing/cleaned_data.json", "r", encoding="utf-8") as f:
        theses_data = json.load(f)
    print(f"Loaded {len(theses_data)} theses from JSON file")
except Exception as e:
    print(f"Error loading JSON data: {e}")
    exit(1)

print("Loading SentenceTransformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully")

index_name = "cs_theses_semantic"

if es.indices.exists(index=index_name):
    print(f"Deleting existing index: {index_name}")
    es.indices.delete(index=index_name)

mapping = {
    "mappings": {
        "properties": {
            "abstract": {"type": "text"},
            "abstract_vector": {
                "type": "dense_vector",
                "dims": model.get_sentence_embedding_dimension(),
                "index": True,
                "similarity": "cosine"
            },
            "author": {"type": "text"},
            "supervisor": {"type": "text"},
            "year": {"type": "integer"},
            "keywords": {"type": "text"}
        }
    }
}

print(f"Creating index with vector mapping: {index_name}")
es.indices.create(index=index_name, body=mapping)

bulk_data = []
for i, thesis in enumerate(theses_data, start=1):
    if not thesis.get("abstract"):
        print(f"Skipping thesis {i} - no abstract")
        continue
    
    try:
        abstract = thesis["abstract"]
        embedding = model.encode(abstract)
        
        thesis_with_embedding = thesis.copy()
        thesis_with_embedding["abstract_vector"] = embedding.tolist()
        
        bulk_data.append({
            "_index": index_name,
            "_id": i,
            "_source": thesis_with_embedding
        })
        
        if i % 10 == 0:
            print(f"Processed {i} theses")
            
    except Exception as e:
        print(f"Error processing thesis {i}: {e}")

if bulk_data:
    print(f"Indexing {len(bulk_data)} theses with embeddings...")
    success, failed = helpers.bulk(es, bulk_data, stats_only=True)
    print(f"Indexed {success} documents, {failed} failed")
else:
    print("No data to index")

print("Semantic index created successfully!")
