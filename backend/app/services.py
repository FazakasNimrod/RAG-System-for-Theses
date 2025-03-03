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
