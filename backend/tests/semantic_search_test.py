from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from services import perform_search, perform_semantic_search
import json

"""
This script tests both regular search and semantic search functionality.
It performs the same search using both methods to show the differences.
"""

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

if not es.ping():
    print("Failed to connect to Elasticsearch.")
    exit(1)

print("Connected to Elasticsearch!")
print("Checking if semantic index exists...")

if not es.indices.exists(index="cs_theses_semantic"):
    print("WARNING: The semantic index 'cs_theses_semantic' does not exist.")
    print("Please run generate_embeddings.py first to create the index.")
    exit(1)

print("Semantic index exists. Proceeding with test.")

test_queries = [
    "machine learning applications",
    "neural networks for image recognition",
    "security in cloud computing",
    "automated testing methods"
]

def print_results(results, search_type, query):
    print(f"\n===== {search_type} SEARCH RESULTS =====")
    print(f"Query: '{query}'")
    print(f"Total results: {len(results)}")
    
    for i, hit in enumerate(results[:5]): 
        source = hit["_source"]
        score = hit.get("_score", "N/A")
        print(f"\nResult #{i+1}: {source.get('author')} ({source.get('year')}) - Score: {score}")
        
        if "highlight" in hit and "abstract" in hit["highlight"]:
            print(f"Abstract snippet: {' ... '.join(hit['highlight']['abstract'])}")
        else:
            abstract = source.get("abstract", "")
            print(f"Abstract snippet: {abstract[:150]}...")
        
        keywords = source.get("keywords", [])
        if keywords:
            print(f"Keywords: {', '.join(keywords)}")

for query in test_queries:
    print("\n" + "="*80)
    print(f"TESTING QUERY: '{query}'")
    print("="*80)
    
    print("\nPerforming regular search...")
    regular_results = perform_search(es, query, None, "desc")
    print_results(regular_results, "REGULAR KEYWORD", query)
    
    print("\nPerforming semantic search...")
    semantic_results = perform_semantic_search(es, query, None, "desc")
    print_results(semantic_results, "SEMANTIC", query)
    
    regular_ids = {hit["_id"] for hit in regular_results}
    semantic_ids = {hit["_id"] for hit in semantic_results}
    
    common_ids = regular_ids.intersection(semantic_ids)
    
    print("\n===== COMPARISON =====")
    print(f"Regular search found {len(regular_results)} results")
    print(f"Semantic search found {len(semantic_results)} results")
    print(f"Number of common results: {len(common_ids)}")
    
    if common_ids:
        print(f"Percentage of common results: {len(common_ids)/max(len(regular_ids), len(semantic_ids))*100:.1f}%")
    else:
        print("No common results between the two search methods")
    
    input("\nPress Enter to continue to the next query...")
    