import csv
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import sys
import json
import numpy as np
from sentence_transformers import SentenceTransformer

from search_services import perform_search, perform_semantic_search

modell_name = 'all-MiniLM-L6-v2'
#modell_name = 'BAAI/bge-small-en' 
#modell_name = 'BAAI/bge-base-en'
#modell_name = 'BAAI/bge-large-en'

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

TEST_DATASET_PATH = "backend/evaluation/test_dataset_classified.csv"
RESULTS_PATH = "backend/evaluation/search_evaluation_results.csv"
DEBUG_LOG_PATH = "backend/evaluation/search_debug.log"

MAX_RESULTS = 50

_model = None

def get_model():
    """Get or initialize the SentenceTransformer model"""
    global _model
    if _model is None:
        print("Loading SentenceTransformer model...")
        _model = SentenceTransformer(modell_name)
        print("Model loaded successfully")
    return _model

def find_document_by_abstract(abstract):
    """
    Find a document in the index by its abstract using vector similarity
    and return its hash_code
    """
    if not abstract or len(abstract.strip()) < 10:
        print("Warning: Abstract is too short or empty")
        return None
    
    abstract = abstract.strip()
    
    model = get_model()
    abstract_vector = model.encode(abstract).tolist()
    
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'abstract_vector') + 1.0",
                    "params": {"query_vector": abstract_vector}
                }
            }
        },
        "size": 1
    }
    
    response = es.search(index="infos_theses_semantic,cs_theses_semantic", body=query)
    
    if response['hits']['hits']:
        doc = response['hits']['hits'][0]['_source']
        similarity_score = response['hits']['hits'][0]['_score']
        print(f"Found similar document with score: {similarity_score}")
        
        hash_code = doc.get("hash_code")
        
        if similarity_score < 1.5: 
            print("Warning: Low similarity score, might not be the correct document")
        
        return hash_code
    
    return None

def normalize_hash_code(hash_code):
    """Normalize hash code to ensure consistent comparison"""
    if hash_code is None:
        return None
    
    if isinstance(hash_code, str):
        try:
            if hash_code.isdigit():
                return int(hash_code)
        except (ValueError, AttributeError):
            pass
    
    return hash_code

def find_rank_in_results(results, hash_code):
    """
    Find the rank (position) of a document with the specified hash_code in the results list
    Returns 0 if not found (which will convert to "not found" later)
    """
    if not hash_code:
        print("Warning: No hash code provided to find_rank_in_results")
        return 0
    
    normalized_ref_hash = normalize_hash_code(hash_code)
    
    total_results = len(results)
    print(f"Searching for hash code {hash_code} in {total_results} results")
    
    for i, hit in enumerate(results):
        hit_hash = hit['_source'].get('hash_code')
        normalized_hit_hash = normalize_hash_code(hit_hash)
        
        if normalized_hit_hash == normalized_ref_hash:
            return i + 1 
    
    print(f"Warning: Document with hash {hash_code} not found in {total_results} results")
    
    if total_results > 0:
        print("First few result hash codes:")
        for i, hit in enumerate(results[:min(5, total_results)]):
            print(f"  Result #{i+1}: {hit['_source'].get('hash_code')}")
    
    return 0 

def log_debug_info(debug_file, user_input, reference_hash, keyword_results, semantic_results):
    """Log detailed debugging information to a file"""
    try:
        with open(debug_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{'='*80}\n")
            f.write(f"QUERY: {user_input}\n")
            f.write(f"{'='*80}\n\n")
            
            try:
                from utils import remove_stop_words
                filtered_query = remove_stop_words(user_input)
                f.write(f"Original query: '{user_input}'\n")
                f.write(f"Filtered query: '{filtered_query}'\n\n")
            except ImportError:
                f.write("Could not import stop_words module for query analysis\n\n")
            
            f.write("REFERENCE DOCUMENT:\n")
            found_ref = False
            for index in ["infos_theses", "cs_theses"]:
                try:
                    query = {"query": {"term": {"hash_code": reference_hash}}}
                    response = es.search(index=index, body=query)
                    if response['hits']['hits']:
                        ref_doc = response['hits']['hits'][0]['_source']
                        f.write(f"Hash: {reference_hash}\n")
                        f.write(f"Author: {ref_doc.get('author')}\n")
                        f.write(f"Department: {ref_doc.get('department', 'unknown')}\n")
                        f.write(f"Year: {ref_doc.get('year', 'unknown')}\n")
                        f.write(f"Abstract: {ref_doc.get('abstract', '')[:200]}...\n\n")
                        found_ref = True
                        break
                except Exception as e:
                    f.write(f"Error searching for document in {index}: {e}\n")
            
            if not found_ref:
                f.write(f"Could not find reference document with hash {reference_hash} in indices\n\n")
            
            f.write(f"Total keyword results: {len(keyword_results)}\n")
            f.write(f"Total semantic results: {len(semantic_results)}\n")
            
            normalized_ref_hash = normalize_hash_code(reference_hash)
            keyword_found = any(normalize_hash_code(hit['_source'].get('hash_code')) == normalized_ref_hash for hit in keyword_results)
            semantic_found = any(normalize_hash_code(hit['_source'].get('hash_code')) == normalized_ref_hash for hit in semantic_results)
            
            f.write(f"Reference document found in keyword results: {keyword_found}\n")
            f.write(f"Reference document found in semantic results: {semantic_found}\n\n")
            
            f.write("KEYWORD SEARCH RESULTS:\n")
            for i, hit in enumerate(keyword_results[:10]): 
                f.write(f"Rank #{i+1} - Hash: {hit['_source'].get('hash_code')} - Score: {hit['_score']}\n")
                f.write(f"Author: {hit['_source'].get('author')}\n")
                f.write(f"Department: {hit['_source'].get('department', 'unknown')}\n")
                f.write(f"Year: {hit['_source'].get('year', 'unknown')}\n")
                f.write(f"Abstract: {hit['_source'].get('abstract', '')[:150]}...\n\n")
            
            f.write("SEMANTIC SEARCH RESULTS:\n")
            for i, hit in enumerate(semantic_results[:10]):
                f.write(f"Rank #{i+1} - Hash: {hit['_source'].get('hash_code')} - Score: {hit['_score']}\n")
                f.write(f"Author: {hit['_source'].get('author')}\n")
                f.write(f"Department: {hit['_source'].get('department', 'unknown')}\n")
                f.write(f"Year: {hit['_source'].get('year', 'unknown')}\n")
                f.write(f"Abstract: {hit['_source'].get('abstract', '')[:150]}...\n\n")
            
    except Exception as e:
        print(f"Error writing debug log: {e}")

def main():
    """
    Main function to run the evaluation
    """
    if not os.path.exists(TEST_DATASET_PATH):
        print(f"Test dataset not found at {TEST_DATASET_PATH}")
        exit(1)
    
    with open(DEBUG_LOG_PATH, 'w', encoding='utf-8') as debug_file:
        debug_file.write("SEARCH EVALUATION DEBUG LOG\n")
        debug_file.write("==========================\n")
        debug_file.write(f"Max results per search: {MAX_RESULTS}\n\n")
    
    with open(RESULTS_PATH, 'w', newline='', encoding='utf-8') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(['user_input', 'reference_hash', 'keyword_search', 'semantic_search'])
        
        with open(TEST_DATASET_PATH, 'r', encoding='utf-8') as dataset_file:
            dataset_reader = csv.reader(dataset_file)
            header = next(dataset_reader)
            
            for i, row in enumerate(dataset_reader):
                print(f"Processing row {i+1}...")
                
                user_input = row[0]
                reference_context = row[1]
                
                reference_hash = find_document_by_abstract(reference_context)
                
                if not reference_hash:
                    print(f"Warning: Reference context not found in index for row {i+1}")
                    results_writer.writerow([user_input, "not found", "not found", "not found"])
                    continue
                
                try:
                    keyword_results = perform_search(es, user_input, None, None, False, None)
                    
                    keyword_rank = find_rank_in_results(keyword_results, reference_hash)
                    
                    semantic_results = perform_semantic_search(es, user_input, None, None, MAX_RESULTS)
                    semantic_rank = find_rank_in_results(semantic_results, reference_hash)
                    
                    log_debug_info(DEBUG_LOG_PATH, user_input, reference_hash, keyword_results, semantic_results)
                    
                    results_writer.writerow([
                        user_input,
                        reference_hash,
                        keyword_rank if keyword_rank > 0 else "not found", 
                        semantic_rank if semantic_rank > 0 else "not found"
                    ])
                    
                    print(f"  Query: {user_input[:50]}...")
                    print(f"  Reference hash: {reference_hash}")
                    print(f"  Keyword rank: {keyword_rank if keyword_rank > 0 else 'not found'}")
                    print(f"  Semantic rank: {semantic_rank if semantic_rank > 0 else 'not found'}")
                    print()
                except Exception as e:
                    print(f"Error processing query '{user_input}': {e}")
                    results_writer.writerow([
                        user_input,
                        reference_hash,
                        "error",
                        "error"
                    ])
    
    print(f"Evaluation completed. Results saved to {RESULTS_PATH}")
    print(f"Debug information saved to {DEBUG_LOG_PATH}")

if __name__ == "__main__":
    main()