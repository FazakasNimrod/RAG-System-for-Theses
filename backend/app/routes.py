from flask import Blueprint, request, jsonify, g
from services import perform_search, perform_semantic_search
from ollama_rag_service import generate_rag_response, get_available_models

search_routes = Blueprint('search', __name__)

@search_routes.route('/', methods=['GET'])
def search():
    """
    Search API for querying Elasticsearch.
    Supports filtering by year, sorting by year, and highlighting matches.
    Add 'phrase=true' query parameter for exact phrase matching.
    Add 'department=cs' or 'department=informatics' to filter by department.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_order = request.args.get('sort', 'desc')
    department = request.args.get('department') 
    
    is_phrase_search = request.args.get('phrase', '').lower() == 'true'

    response = perform_search(es, query, year, sort_order, is_phrase_search, department)

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
    department = request.args.get('department') 

    if not query:
        return jsonify([])

    try:
        response = perform_semantic_search(es, query, year, sort_order, limit, department)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Semantic search failed: {str(e)}"}), 500

@search_routes.route('/rag', methods=['POST'])
def rag():
    """
    RAG API for question answering over thesis documents.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    data = request.json
    query = data.get('query', '')
    model_id = data.get('model', 'llama3.2:3b')
    top_k = data.get('top_k', 5)
    department = data.get('department')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        response = generate_rag_response(es, query, model_id, top_k, department)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"RAG processing failed: {str(e)}"}), 500

@search_routes.route('/models', methods=['GET'])
def models():
    try:
        models = get_available_models()
        return jsonify(models)
    except Exception as e:
        return jsonify({"error": f"Failed to get models: {str(e)}"}), 500
    
@search_routes.route('/departments', methods=['GET'])
def get_departments():
    """
    API endpoint to get available departments
    """
    departments = [
        {"id": "cs", "name": "Computer Science"},
        {"id": "informatics", "name": "Informatics"}
    ]
    return jsonify(departments)    
    