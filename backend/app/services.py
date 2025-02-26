def perform_search(es, query, year, sort_order):
    """
    Perform a search query in Elasticsearch.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :return: Search results as a dictionary
    """
    search_query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["abstract", "keywords^2", "author"]
                    }
                },
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
