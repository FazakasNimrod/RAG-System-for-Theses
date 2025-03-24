from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import json

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

def get_all_documents(index_name, size=100):
    query = {
        "query": {
            "match_all": {}
        },
        "size": size
    }
    
    response = es.search(index=index_name, body=query)
    return response['hits']['hits']

infos_docs = get_all_documents("infos_theses")
print(f"Found {len(infos_docs)} documents in infos_theses index")

if infos_docs:
    print("\nSample document:")
    sample_doc = infos_docs[0]["_source"]
    print(json.dumps(sample_doc, indent=2, ensure_ascii=False))

    print("\nAll authors in the index:")
    for doc in infos_docs:
        print(f"- {doc['_source']['author']}")

semantic_docs = get_all_documents("infos_theses_semantic")
print(f"\nFound {len(semantic_docs)} documents in infos_theses_semantic index")
