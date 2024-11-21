from flask import Blueprint, request, jsonify, g
from services import perform_search  # Import the search function from services.py

# Create a Blueprint for the search routes
search_routes = Blueprint('search', __name__)

@search_routes.route('/', methods=['GET'])
def search():
    """
    Search API for querying Elasticsearch.
    Supports filtering by year, sorting by year, and highlighting matches.
    """
    es = getattr(g, 'es', None)  # Get 'es' from the Flask global context (g)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    query = request.args.get('q', '')  # Search query
    year = request.args.get('year')   # Optional filter by year
    sort_order = request.args.get('sort', 'desc')  # Optional sort order, default is 'desc'

    # Call the search function from services.py
    response = perform_search(es, query, year, sort_order)

    # Return the search results
    return jsonify(response)
