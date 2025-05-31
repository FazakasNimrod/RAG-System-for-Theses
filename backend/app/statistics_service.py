from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional

def get_statistics(es, department: str = None, year: int = None, supervisor: str = None):
    """
    Get comprehensive statistics from the thesis database.
    
    :param es: Elasticsearch client instance
    :param department: Optional filter by department ('cs' or 'informatics')
    :param year: Optional filter by year
    :param supervisor: Optional filter by supervisor
    :return: Dictionary containing various statistics
    """
    print(f"Getting statistics with filters - department: {department}, year: {year}, supervisor: {supervisor}")
    
    filters = []
    if department:
        filters.append({"term": {"department": department}})
    if year:
        filters.append({"term": {"year": year}})
    if supervisor:
        filters.append({
            "bool": {
                "should": [
                    {"term": {"supervisor.keyword": supervisor}},
                    {"match": {"supervisor": supervisor}}
                ]
            }
        })
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]
    
    print(f"Searching indices: {indices} with {len(filters)} filters")
    
    base_query = {
        "query": {
            "bool": {
                "filter": filters
            }
        } if filters else {"match_all": {}},
        "size": 10000
    }
    
    try:
        response = es.search(index=",".join(indices), body=base_query)
        documents = response['hits']['hits']
        
        print(f"Found {len(documents)} documents matching filters")
        
        stats = calculate_document_statistics(documents)
        
        return {
            "success": True,
            "total_documents": len(documents),
            "statistics": stats,
            "filters_applied": {
                "department": department,
                "year": year,
                "supervisor": supervisor
            }
        }
        
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {
            "success": False,
            "error": str(e),
            "total_documents": 0,
            "statistics": {},
            "filters_applied": {}
        }

def calculate_document_statistics(documents: List[Dict]) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics from a list of documents.
    
    :param documents: List of Elasticsearch document hits
    :return: Dictionary containing calculated statistics
    """
    if not documents:
        return {
            "by_year": {},
            "by_department": {},
            "by_supervisor": {},
            "top_keywords": {},
            "year_range": {"min": None, "max": None},
            "average_abstract_length": 0,
            "supervisors_count": 0,
            "recent_theses": []
        }
    
    years = []
    departments = []
    supervisors = []
    keywords = []
    abstract_lengths = []
    all_docs = []
    
    for hit in documents:
        source = hit['_source']
        
        if source.get('year'):
            years.append(int(source['year']))
        
        if source.get('department'):
            departments.append(source['department'])
        
        supervisor_field = source.get('supervisor', [])
        if supervisor_field:
            if isinstance(supervisor_field, str):
                if ',' in supervisor_field:
                    supervisor_parts = [part.strip() for part in supervisor_field.split(',')]
                    for part in supervisor_parts:
                        if part:
                            supervisors.append(part)
                else:
                    supervisors.append(supervisor_field.strip())
            elif isinstance(supervisor_field, list):
                for sup in supervisor_field:
                    if sup and isinstance(sup, str) and sup.strip():
                        supervisors.append(sup.strip())
        
        keyword_field = source.get('keywords', [])
        if isinstance(keyword_field, str):
            keywords.extend([kw.strip() for kw in keyword_field.split(',') if kw.strip()])
        elif isinstance(keyword_field, list):
            keywords.extend([kw.strip() for kw in keyword_field if kw and kw.strip()])
        
        abstract = source.get('abstract', '')
        if abstract:
            abstract_lengths.append(len(abstract))
        
        display_supervisor = supervisor_field
        if isinstance(supervisor_field, list):
            display_supervisor = supervisor_field
        elif isinstance(supervisor_field, str) and ',' in supervisor_field:
            display_supervisor = [part.strip() for part in supervisor_field.split(',') if part.strip()]
        
        all_docs.append({
            'author': source.get('author', 'Unknown'),
            'year': source.get('year', 'Unknown'),
            'department': source.get('department', 'Unknown'),
            'supervisor': display_supervisor,
            'hash_code': source.get('hash_code')
        })
    
    year_counts = Counter(years)
    department_counts = Counter(departments)
    supervisor_counts = Counter(supervisors)
    keyword_counts = Counter(keywords)
    
    current_year = max(years) if years else 2023
    recent_theses = [
        doc for doc in all_docs 
        if doc['year'] != 'Unknown' and int(doc['year']) >= current_year - 2
    ]
    recent_theses.sort(key=lambda x: int(x['year']) if x['year'] != 'Unknown' else 0, reverse=True)
    
    return {
        "by_year": dict(sorted(year_counts.items())),
        "by_department": dict(department_counts),
        "by_supervisor": dict(sorted(supervisor_counts.items(), key=lambda x: x[1], reverse=True)[:20]), 
        "top_keywords": dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:15]), 
        "year_range": {
            "min": min(years) if years else None,
            "max": max(years) if years else None
        },
        "average_abstract_length": int(sum(abstract_lengths) / len(abstract_lengths)) if abstract_lengths else 0,
        "supervisors_count": len(set(supervisors)),
        "recent_theses": recent_theses[:10] 
    }

def get_unique_supervisors(es, department: str = None):
    """
    Get a list of unique supervisors for filter dropdown.
    
    :param es: Elasticsearch client instance
    :param department: Optional filter by department
    :return: List of unique supervisor names
    """
    print(f"Getting supervisors for department: {department}")
    
    filters = []
    if department:
        filters.append({"term": {"department": department}})
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]
    
    print(f"Searching indices: {indices}")

    try:
        if filters:
            manual_query = {
                "query": {
                    "bool": {"filter": filters}
                },
                "size": 10000,
                "_source": ["supervisor"]
            }
        else:
            manual_query = {
                "query": {"match_all": {}},
                "size": 10000,
                "_source": ["supervisor"]
            }
        
        print(f"Query: {manual_query}")
        
        response = es.search(index=",".join(indices), body=manual_query)
        supervisor_set = set()
        
        print(f"Processing {len(response['hits']['hits'])} documents")
        
        for hit in response['hits']['hits']:
            supervisor_field = hit['_source'].get('supervisor')
            
            if supervisor_field:
                if isinstance(supervisor_field, list):
                    for sup in supervisor_field:
                        if sup and isinstance(sup, str) and sup.strip():
                            supervisor_set.add(sup.strip())
                elif isinstance(supervisor_field, str):
                    if supervisor_field.strip():
                        supervisor_set.add(supervisor_field.strip())
        
        supervisors = sorted(list(supervisor_set))
        print(f"Found {len(supervisors)} unique supervisors")
        return supervisors
        
    except Exception as e:
        print(f"Error extracting supervisors: {e}")
        return []

def get_unique_years(es, department: str = None):
    """
    Get a list of unique years for filter dropdown.
    
    :param es: Elasticsearch client instance
    :param department: Optional filter by department
    :return: List of unique years
    """
    filters = []
    if department:
        filters.append({"term": {"department": department}})
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]

    try:
        if filters:
            manual_query = {
                "query": {
                    "bool": {"filter": filters}
                },
                "size": 10000,
                "_source": ["year"]
            }
        else:
            manual_query = {
                "query": {"match_all": {}},
                "size": 10000,
                "_source": ["year"]
            }
        
        response = es.search(index=",".join(indices), body=manual_query)
        year_set = set()
        
        for hit in response['hits']['hits']:
            year_field = hit['_source'].get('year')
            if year_field:
                try:
                    year_int = int(year_field)
                    year_set.add(year_int)
                except (ValueError, TypeError):
                    pass
        
        years = sorted(list(year_set), reverse=True) 
        return years
        
    except Exception as e:
        print(f"Error extracting years: {e}")
        return []
    