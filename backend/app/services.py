def perform_search(es, query, year, sort_order):
    """
    Perform a search query in Elasticsearch.

    :param es: Elasticsearch client instance
    :param query: Search query string
    :param year: Optional filter by year
    :param sort_order: Sorting order ('desc' or 'asc')
    :return: Search results as a dictionary
    """
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

    # Execute the search query
    response = es.search(index="theses", body=search_query)

    # Return the search results (hits) with highlighting
    return response['hits']['hits']
