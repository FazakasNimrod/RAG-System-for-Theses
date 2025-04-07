from dotenv import load_dotenv
import os
import json
from elasticsearch import Elasticsearch, helpers

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

CS_CLEANED_DATA_PATH = "backend\scripts\pdf_processing\cs_pdf_processing\cleaned_data.json"
INFOS_CLEANED_DATA_PATH = "backend\scripts\pdf_processing\info_pdf_processing\cleaned_infos_data.json"

INDICES_MAP = {
    "cs": ["cs_theses", "cs_theses_semantic"],
    "informatics": ["infos_theses", "infos_theses_semantic"]
}

def load_cleaned_data():
    """
    Load cleaned data from JSON files
    """
    cs_data = []
    infos_data = []
    
    try:
        with open(CS_CLEANED_DATA_PATH, 'r', encoding='utf-8') as f:
            cs_data = json.load(f)
        print(f"Loaded {len(cs_data)} documents from cleaned CS data")
    except Exception as e:
        print(f"Error loading CS data: {e}")
    
    try:
        with open(INFOS_CLEANED_DATA_PATH, 'r', encoding='utf-8') as f:
            infos_data = json.load(f)
        print(f"Loaded {len(infos_data)} documents from cleaned Informatics data")
    except Exception as e:
        print(f"Error loading Informatics data: {e}")
    
    return {
        "cs": cs_data,
        "informatics": infos_data
    }

def update_indices_with_hash_codes():
    """
    Update Elasticsearch indices with hash codes from cleaned data files
    """
    if not es.ping():
        print("Failed to connect to Elasticsearch")
        return
    
    print("Connected to Elasticsearch!")
    
    cleaned_data = load_cleaned_data()
    
    for dept, data in cleaned_data.items():
        if not data:
            print(f"No data for department: {dept}")
            continue
        
        author_to_hash = {}
        for doc in data:
            author = doc.get("author", "").lower()
            hash_code = doc.get("hash_code")
            if author and hash_code:
                author_to_hash[author] = hash_code
        
        indices = INDICES_MAP.get(dept, [])
        for index_name in indices:
            print(f"\nProcessing index: {index_name}")
            
            if not es.indices.exists(index=index_name):
                print(f"Index {index_name} does not exist. Skipping.")
                continue
            
            try:
                mapping = es.indices.get_mapping(index=index_name)
                properties = mapping[index_name]['mappings']['properties']
                
                if 'hash_code' not in properties:
                    print(f"Adding hash_code field to {index_name}")
                    es.indices.put_mapping(
                        index=index_name,
                        body={
                            "properties": {
                                "hash_code": {"type": "long"}
                            }
                        }
                    )
            except Exception as e:
                print(f"Error checking/updating mapping: {e}")
                continue
            
            try:
                query = {"query": {"match_all": {}}, "size": 1000}
                response = es.search(index=index_name, body=query)
                docs = response["hits"]["hits"]
                
                print(f"Found {len(docs)} documents in index {index_name}")
                updated_count = 0
                
                bulk_actions = []
                for doc in docs:
                    doc_id = doc["_id"]
                    source = doc["_source"]
                    author = source.get("author", "").lower()
                    
                    hash_code = author_to_hash.get(author)
                    
                    if hash_code is not None:
                        bulk_actions.append({
                            "_op_type": "update",
                            "_index": index_name,
                            "_id": doc_id,
                            "doc": {
                                "hash_code": hash_code
                            }
                        })
                        updated_count += 1
                
                if bulk_actions:
                    print(f"Updating {len(bulk_actions)} documents in {index_name}...")
                    success, failed = helpers.bulk(es, bulk_actions, stats_only=True)
                    print(f"Updated {success} documents, {failed} failed")
                else:
                    print(f"No documents to update in {index_name}")
                
            except Exception as e:
                print(f"Error updating index {index_name}: {e}")

def main():
    update_indices_with_hash_codes()
    print("\nFinished updating Elasticsearch indices with hash codes")

if __name__ == "__main__":
    main()
    