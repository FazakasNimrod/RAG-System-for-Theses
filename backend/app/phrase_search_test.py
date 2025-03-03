from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from services import perform_search
import json

"""
This script tests both regular search and phrase search functionality.
It performs the same search with and without phrase matching to show the difference.
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

test_query = "deep learning"

def print_results(results, search_type):
    print(f"\n===== {search_type} SEARCH RESULTS =====")
    print(f"Query: '{test_query}'")
    print(f"Total results: {len(results)}")
    
    for i, hit in enumerate(results[:5]): 
        source = hit["_source"]
        print(f"\nResult #{i+1}: {source.get('author')} ({source.get('year')})")
        
        if "highlight" in hit and "abstract" in hit["highlight"]:
            print(f"Abstract snippet: {' ... '.join(hit['highlight']['abstract'])}")
        else:
            abstract = source.get("abstract", "")
            print(f"Abstract snippet: {abstract[:150]}...")

print("\nPerforming regular search...")
regular_results = perform_search(es, test_query, None, "desc", is_phrase_search=False)
print_results(regular_results, "REGULAR")

print("\nPerforming phrase search...")
phrase_results = perform_search(es, test_query, None, "desc", is_phrase_search=True)
print_results(phrase_results, "PHRASE")

regular_ids = {hit["_id"] for hit in regular_results}
phrase_ids = {hit["_id"] for hit in phrase_results}

print("\n===== COMPARISON =====")
print(f"Regular search found {len(regular_results)} results")
print(f"Phrase search found {len(phrase_results)} results")

if phrase_ids.issubset(regular_ids):
    print("All phrase search results are also found in regular search (as expected)")
    
    filtered_count = len(regular_ids) - len(phrase_ids)
    if filtered_count > 0:
        print(f"Phrase search filtered out {filtered_count} results that didn't contain the exact phrase")
    else:
        print("All regular search results also contain the exact phrase")
else:
    print("WARNING: Some phrase search results are not in regular search results (unexpected)")
    