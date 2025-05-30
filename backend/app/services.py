from sentence_transformers import SentenceTransformer
from stop_words import remove_stop_words, get_important_terms

modell_name = 'all-MiniLM-L6-v2'
#modell_name = 'BAAI/bge-small-en' 
#modell_name = 'BAAI/bge-base-en'
#modell_name = 'BAAI/bge-large-en'

def perform_search(es, query, year=None, sort_order=None, is_phrase_search=False, department=None, search_supervisors=False):
    """
    Perform a search query in Elasticsearch.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc') for year-based sorting. 
                       If None, sort by relevance only.
    :param is_phrase_search: Whether to perform a phrase search (exact match)
    :param department: Optional filter by department ('cs' or 'informatics')
    :param search_supervisors: Whether to include supervisor field in search
    :return: Search results as a dictionary
    """
    if not query:
        return []
        
    if search_supervisors:
        if is_phrase_search:
            search_fields = {
                "match_phrase": {"supervisor": query}
            }
        else:
            filtered_query = remove_stop_words(query)
            print(f"Original query: '{query}' -> Filtered query: '{filtered_query}' (supervisor search only)")
            
            if not filtered_query.strip():
                filtered_query = query
            
            search_fields = {
                "match": {
                    "supervisor": {
                        "query": filtered_query,
                        "operator": "OR"
                    }
                }
            }
    else:
        if is_phrase_search:
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
            filtered_query = remove_stop_words(query)
            print(f"Original query: '{query}' -> Filtered query: '{filtered_query}'")
            
            if not filtered_query.strip():
                filtered_query = query
            
            search_fields = {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "abstract": {
                                    "query": filtered_query,
                                    "operator": "OR",
                                    "minimum_should_match": "60%",
                                    "boost": 1.0
                                }
                            }
                        },
                        {
                            "match": {
                                "keywords": {
                                    "query": filtered_query,
                                    "boost": 2.0
                                }
                            }
                        },
                        {
                            "match": {
                                "author": {
                                    "query": filtered_query,
                                    "boost": 0.5
                                }
                            }
                        }
                    ]
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
        "highlight": {
            "fields": {}
        },
        "size": 10 
    }
    
    if search_supervisors:
        search_query["highlight"]["fields"]["supervisor"] = {}
    else:
        search_query["highlight"]["fields"]["abstract"] = {}
        search_query["highlight"]["fields"]["keywords"] = {}
    
    if sort_order in ["asc", "desc"]:
        search_query["sort"] = [
            {"year": {"order": sort_order}},  
            "_score"  
        ]
    else:
        search_query["sort"] = ["_score"]

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
        _model = SentenceTransformer(modell_name)
    return _model

def perform_semantic_search(es, query, year=None, sort_order=None, num_results=100, department=None):
    """
    Perform a semantic search query in Elasticsearch using vector embeddings.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc') for year-based sorting.
                       If None, sort by relevance only.
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
            {"year": {"order": sort_order}}, 
        ]
    else:
        search_query["sort"] = ["_score"]  
    
    if department == "cs":
        indices = ["cs_theses_semantic"]
    elif department == "informatics":
        indices = ["infos_theses_semantic"]
    else:
        indices = ["cs_theses_semantic", "infos_theses_semantic"] 
    
    response = es.search(index=",".join(indices), body=search_query)
    
    return response['hits']['hits']

def get_document_by_hash(es, hash_code, department=None):
    """
    Retrieve a document by its hash code.

    :param es: Elasticsearch client instance
    :param hash_code: The hash code of the document to retrieve
    :param department: Optional filter by department ('cs' or 'informatics')
    :return: The document or None if not found
    """
    filter_clause = [{"term": {"hash_code": hash_code}}]
    
    if department:
        filter_clause.append({"term": {"department": department}})
    
    search_query = {
        "query": {
            "bool": {
                "filter": filter_clause
            }
        },
        "size": 1
    }
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]
    
    try:
        response = es.search(index=",".join(indices), body=search_query)
        hits = response['hits']['hits']
        if hits:
            return hits[0]
        return None
    except Exception as e:
        print(f"Error retrieving document by hash: {e}")
        return None