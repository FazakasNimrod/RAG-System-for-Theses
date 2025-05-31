from flask import Blueprint, request, jsonify, g, redirect
from services import perform_search, perform_semantic_search, get_document_by_hash
from ollama_rag_service import generate_rag_response, get_available_models

try:
    from statistics_service import get_statistics, get_unique_supervisors, get_unique_years
    print("Successfully imported statistics functions")
except ImportError as e:
    print(f"Failed to import statistics functions: {e}")
    def get_statistics(es, department=None, year=None, supervisor=None):
        return {"success": False, "error": "Statistics service not available"}
    def get_unique_supervisors(es, department=None):
        return []
    def get_unique_years(es, department=None):
        return []

search_routes = Blueprint('search', __name__)

@search_routes.route('/', methods=['GET'])
def search():
    """
    Search API for querying Elasticsearch.
    Supports filtering by year, sorting by year, and highlighting matches.
    Add 'phrase=true' query parameter for exact phrase matching.
    Add 'department=cs' or 'department=informatics' to filter by department.
    Add 'search_supervisors=true' to include supervisor field in search.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_order = request.args.get('sort', 'desc')
    department = request.args.get('department') 
    
    is_phrase_search = request.args.get('phrase', '').lower() == 'true'
    search_supervisors = request.args.get('search_supervisors', '').lower() == 'true'

    response = perform_search(es, query, year, sort_order, is_phrase_search, department, search_supervisors)

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

@search_routes.route('/statistics', methods=['GET'])
def statistics():
    """
    Get statistics about theses with optional filtering.
    Supports filtering by department, year, and supervisor.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    department = request.args.get('department')
    year = request.args.get('year', type=int)
    supervisor = request.args.get('supervisor')

    try:
        stats = get_statistics(es, department, year, supervisor)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": f"Statistics failed: {str(e)}"}), 500

@search_routes.route('/statistics/supervisors', methods=['GET'])
def statistics_supervisors():
    """
    Get unique supervisors for statistics filtering.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    department = request.args.get('department')
    
    print(f"API: Getting supervisors for department: {department}")

    try:
        supervisors = get_unique_supervisors(es, department)
        print(f"API: Returning {len(supervisors)} supervisors")
        return jsonify(supervisors)
    except Exception as e:
        print(f"API: Error getting supervisors: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to get supervisors: {str(e)}"}), 500

@search_routes.route('/statistics/years', methods=['GET'])
def statistics_years():
    """
    Get unique years for statistics filtering.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    department = request.args.get('department')

    try:
        years = get_unique_years(es, department)
        return jsonify(years)
    except Exception as e:
        return jsonify({"error": f"Failed to get years: {str(e)}"}), 500

@search_routes.route('/document/<int:hash_code>', methods=['GET'])
def get_document(hash_code):
    """
    Get a document by its hash code.
    """
    es = getattr(g, 'es', None)

    if not es:
        return jsonify({"error": "Elasticsearch connection is not available."}), 500

    department = request.args.get('department')
    document = get_document_by_hash(es, hash_code, department)
    
    if document:
        return jsonify(document)
    return jsonify({"error": "Document not found"}), 404

@search_routes.route('/pdf/<int:hash_code>', methods=['GET'])
def view_pdf(hash_code):
    """
    Redirect to the PDF storage service to view a PDF by its hash code.
    """
    pdf_storage_url = "http://localhost:5000"
    
    return redirect(f"{pdf_storage_url}/{hash_code}")
