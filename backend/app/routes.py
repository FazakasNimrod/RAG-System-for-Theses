from flask import Blueprint, request, jsonify, g
from services import perform_search, perform_semantic_search

search_routes = Blueprint('search', __name__)

@search_routes.route('/', methods=['GET'])
def search():
    """
    Search API for querying Elasticsearch.
    Supports filtering by year, sorting by year, and highlighting matches.
    Add 'phrase=true' query parameter for exact phrase matching.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_order = request.args.get('sort', 'desc')
    
    is_phrase_search = request.args.get('phrase', '').lower() == 'true'

    response = perform_search(es, query, year, sort_order, is_phrase_search)

    return jsonify(response)

@search_routes.route('/semantic', methods=['GET'])
def semantic_search():
    """
    Semantic search API using vector embeddings.
    Queries are transformed into vectors and compared using cosine similarity.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_order = request.args.get('sort', 'desc')
    limit = request.args.get('limit', 10, type=int)

    if not query:
        return jsonify([])

    try:
        response = perform_semantic_search(es, query, year, sort_order, limit)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Semantic search failed: {str(e)}"}), 500