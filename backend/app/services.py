from sentence_transformers import SentenceTransformer

def perform_search(es, query, year, sort_order, is_phrase_search=False):
    """
    Perform a search query in Elasticsearch.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :param is_phrase_search: Whether to perform a phrase search (exact match)
    :return: Search results as a dictionary
    """
    if is_phrase_search and query:
        search_fields = {
            "bool": {
                "should": [
                    {"match_phrase": {"abstract": query}},
                    {"match_phrase": {"keywords": {"query": query, "boost": 2}}},
                    {"match_phrase": {"author": query}}
                ]
            }
        }
    else:
        search_fields = {
            "multi_match": {
                "query": query,
                "fields": ["abstract", "keywords^2", "author"]
            }
        }

    search_query = {
        "query": {
            "bool": {
                "must": search_fields,
                "filter": [{"term": {"year": int(year)}}] if year else []
            }
        },
        "sort": [{"year": {"order": sort_order}}],
        "highlight": {
            "fields": {
                "abstract": {},
                "keywords": {}
            }
        }
    }

    response = es.search(index="cs_theses", body=search_query)

    return response['hits']['hits']

_model = None

def get_model():
    """Get or initialize the SentenceTransformer model"""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def perform_semantic_search(es, query, year=None, sort_order="desc", num_results=10):
    """
    Perform a semantic search query in Elasticsearch using vector embeddings.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :param num_results: Number of results to return
    :return: Search results as a dictionary
    """
    if not query:
        return []

    model = get_model()
    query_vector = model.encode(query).tolist()
    
    filter_clause = [{"term": {"year": int(year)}}] if year else []
    
    search_query = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "filter": filter_clause
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'abstract_vector') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        },
        "size": num_results,
        "highlight": {
            "fields": {
                "abstract": {},
                "keywords": {}
            }
        }
    }
    
    if sort_order in ["asc", "desc"]:
        search_query["sort"] = [
            "_score",
            {"year": {"order": sort_order}}  
        ]
    
    response = es.search(index="cs_theses_semantic", body=search_query)
    
    return response['hits']['hits']