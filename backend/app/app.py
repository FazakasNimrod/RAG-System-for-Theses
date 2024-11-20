from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials from .env
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")  # Default to 'elastic' if not set

# Connect to Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

# Initialize Flask app
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    """
    Search API for querying Elasticsearch.
    Supports filtering by year, sorting by year, and highlighting matches.
    """
    query = request.args.get('q', '')  # Search query
    year = request.args.get('year')   # Optional filter by year
    sort_order = request.args.get('sort', 'desc')  # Optional sort order, default is 'desc'

    # Build the search query
    search_query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["abstract", "keywords^2", "author"]  # Boost 'keywords' with ^2
                    }
                },
                "filter": [{"term": {"year": int(year)}}] if year else []  # Add year filter if provided
            }
        },
        "sort": [{"year": {"order": sort_order}}],  # Sort by year
        "highlight": {
            "fields": {
                "abstract": {},  # Highlight matches in the abstract
                "keywords": {}   # Highlight matches in keywords
            }
        }
    }

    # Execute the query
    response = es.search(index="theses", body=search_query)

    # Return hits with highlighting (if available)
    return jsonify(response['hits']['hits'])

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
