from sentence_transformers import SentenceTransformer

def perform_search(es, query, year=None, sort_order="desc", is_phrase_search=False, department=None):
    """
    Perform a search query in Elasticsearch.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :param is_phrase_search: Whether to perform a phrase search (exact match)
    :param department: Optional filter by department ('cs' or 'informatics')
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

    filters = []
    if year:
        filters.append({"term": {"year": int(year)}})
    
    if department:
        filters.append({"term": {"department": department}})

    search_query = {
        "query": {
            "bool": {
                "must": search_fields,
                "filter": filters
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

    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"] 

    response = es.search(index=",".join(indices), body=search_query)

    return response['hits']['hits']

_model = None

def get_model():
    """Get or initialize the SentenceTransformer model"""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def perform_semantic_search(es, query, year=None, sort_order="desc", num_results=10, department=None):
    """
    Perform a semantic search query in Elasticsearch using vector embeddings.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :param num_results: Number of results to return
    :param department: Optional filter by department ('cs' or 'informatics')
    :return: Search results as a dictionary
    """
    if not query:
        return []

    model = get_model()
    query_vector = model.encode(query).tolist()
    
    filter_clause = []
    if year:
        filter_clause.append({"term": {"year": int(year)}})
    
    if department:
        filter_clause.append({"term": {"department": department}})
    
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
    
    if department == "cs":
        indices = ["cs_theses_semantic"]
    elif department == "informatics":
        indices = ["infos_theses_semantic"]
    else:
        indices = ["cs_theses_semantic", "infos_theses_semantic"] 
    
    response = es.search(index=",".join(indices), body=search_query)
    
    return response['hits']['hits']