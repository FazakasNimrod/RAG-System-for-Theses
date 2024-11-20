from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the mapping for the 'theses' index
index_mapping = {
    "mappings": {
        "properties": {
            "author": {"type": "text"},
            "year": {"type": "integer"},
            "abstract": {"type": "text"},
            "keywords": {"type": "keyword"}  # 'keyword' type for non-analyzed field (exact match)
        }
    }
}

# Create the index with the mapping
es.indices.create(index="theses", body=index_mapping, ignore=400)  # Ignore 400 if the index already exists
