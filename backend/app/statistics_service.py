from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional
import re
import string

def normalize_keyword(keyword: str) -> str:
    """
    Normalize a keyword to handle duplicates and variations.
    
    :param keyword: Raw keyword string
    :return: Normalized keyword string
    """
    if not keyword or not isinstance(keyword, str):
        return ""

    normalized = keyword.lower().strip()

    normalized = normalized.strip(string.punctuation + ' ')
    
    normalized = re.sub(r'[.,;:!?()"\']', '', normalized)
    
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = re.sub(r'-+', '-', normalized)
    
    keyword_mappings = {
        'javascript': 'JavaScript',
        'python': 'Python',
        'java': 'Java',
        'react': 'React',
        'angular': 'Angular',
        'vue': 'Vue',
        'nodejs': 'Node.js',
        'node.js': 'Node.js',
        'node js': 'Node.js',
        
        'machine learning': 'Machine Learning',
        'machine-learning': 'Machine Learning',
        'ml': 'Machine Learning',
        'artificial intelligence': 'Artificial Intelligence',
        'artificial-intelligence': 'Artificial Intelligence',
        'ai': 'Artificial Intelligence',
        'deep learning': 'Deep Learning',
        'deep-learning': 'Deep Learning',
        'neural networks': 'Neural Networks',
        'neural-networks': 'Neural Networks',
        'cnn': 'CNN',
        'convolutional neural networks': 'CNN',
        'rnn': 'RNN',
        
        'mysql': 'MySQL',
        'postgresql': 'PostgreSQL',
        'mongodb': 'MongoDB',
        'database': 'Database',
        'db': 'Database',
        
        'html': 'HTML',
        'css': 'CSS',
        'web application': 'Web Application',
        'web app': 'Web Application',
        'webapp': 'Web Application',
        'web-application': 'Web Application',
        'mobile app': 'Mobile Application',
        'mobile application': 'Mobile Application',
        'mobile-application': 'Mobile Application',
        
        'spring boot': 'Spring Boot',
        'spring-boot': 'Spring Boot',
        'express': 'Express.js',
        'express.js': 'Express.js',
        'expressjs': 'Express.js',
        'flask': 'Flask',
        'django': 'Django',
        
        'iot': 'IoT',
        'internet of things': 'IoT',
        'api': 'API',
        'rest api': 'REST API',
        'rest-api': 'REST API',
        'restapi': 'REST API',
        'bluetooth': 'Bluetooth',
        'wifi': 'WiFi',
        'wi-fi': 'WiFi',
        
        'image processing': 'Image Processing',
        'image-processing': 'Image Processing',
        'opencv': 'OpenCV',
        'computer vision': 'Computer Vision',
        'computer-vision': 'Computer Vision',
        
        'arduino': 'Arduino',
        'raspberry pi': 'Raspberry Pi',
        'raspberry-pi': 'Raspberry Pi',
        'esp32': 'ESP32',
        'microcontroller': 'Microcontroller',
        'fpga': 'FPGA',
        
        'user interface': 'User Interface',
        'user-interface': 'User Interface',
        'ui': 'User Interface',
        'user experience': 'User Experience',
        'user-experience': 'User Experience',
        'ux': 'User Experience',
        'algorithm': 'Algorithm',
        'algorithms': 'Algorithm',
        'data mining': 'Data Mining',
        'data-mining': 'Data Mining',
        'data analysis': 'Data Analysis',
        'data-analysis': 'Data Analysis',
 
        'medical imaging': 'Medical Imaging',
        'medical-imaging': 'Medical Imaging',
        'healthcare': 'Healthcare',
        'health care': 'Healthcare',
        'telemedicine': 'Telemedicine',
        
        'cybersecurity': 'Cybersecurity',
        'cyber security': 'Cybersecurity',
        'cyber-security': 'Cybersecurity',
        'encryption': 'Encryption',
        'authentication': 'Authentication',
        'security': 'Security',
        
        'network': 'Network',
        'networking': 'Network',
        'wireless': 'Wireless',
        'protocol': 'Protocol',
        'protocols': 'Protocol',
    }
    
    if normalized in keyword_mappings:
        return keyword_mappings[normalized]
    
    return normalized.title() if normalized else ""

def extract_and_normalize_keywords(keyword_field) -> List[str]:
    """
    Extract and normalize keywords from various field formats.
    
    :param keyword_field: Keywords in string or list format
    :return: List of normalized keywords
    """
    keywords = []
    
    if isinstance(keyword_field, str):
        if ',' in keyword_field:
            keywords = [kw.strip() for kw in keyword_field.split(',') if kw.strip()]
        elif ';' in keyword_field:
            keywords = [kw.strip() for kw in keyword_field.split(';') if kw.strip()]
        elif keyword_field.strip():
            keywords = [keyword_field.strip()]
    elif isinstance(keyword_field, list):
        keywords = [kw.strip() for kw in keyword_field if kw and isinstance(kw, str) and kw.strip()]

    normalized_keywords = []
    for keyword in keywords:
        normalized = normalize_keyword(keyword)
        if normalized and len(normalized) > 1:
            normalized_keywords.append(normalized)
    
    return normalized_keywords

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

    if supervisor:
        return get_supervisor_specific_statistics(es, supervisor, department, year)

    filters = []
    if department:
        filters.append({"term": {"department": department}})
    if year:
        filters.append({"term": {"year": year}})
    
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

def get_supervisor_specific_statistics(es, supervisor: str, department: str = None, year: int = None):
    """
    Get statistics specifically for a selected supervisor by finding ALL their theses.
    
    :param es: Elasticsearch client instance
    :param supervisor: The supervisor name to filter by
    :param department: Optional filter by department
    :param year: Optional filter by year
    :return: Dictionary containing supervisor-specific statistics
    """
    print(f"Getting supervisor-specific statistics for: {supervisor}")
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]
    
    supervisor_query = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"supervisor.keyword": supervisor}},
                    {"match": {"supervisor": supervisor}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 10000
    }
    
    try:
        response = es.search(index=",".join(indices), body=supervisor_query)
        all_supervisor_documents = response['hits']['hits']
        
        print(f"Found {len(all_supervisor_documents)} total documents for supervisor: {supervisor}")
        
        filtered_documents = []
        for hit in all_supervisor_documents:
            source = hit['_source']
            supervisor_field = source.get('supervisor', [])

            is_supervised_by = False
            if isinstance(supervisor_field, str):
                if ',' in supervisor_field:
                    supervisor_list = [s.strip() for s in supervisor_field.split(',')]
                    is_supervised_by = supervisor in supervisor_list
                else:
                    is_supervised_by = supervisor_field.strip() == supervisor
            elif isinstance(supervisor_field, list):
                is_supervised_by = supervisor in [s.strip() for s in supervisor_field if s]
            
            if is_supervised_by:
                if year and source.get('year') != year:
                    continue
                if department and source.get('department') != department:
                    continue
                filtered_documents.append(hit)
        
        print(f"After exact matching and filters: {len(filtered_documents)} documents")
        
        stats = calculate_supervisor_specific_statistics(filtered_documents, supervisor)
        
        return {
            "success": True,
            "total_documents": len(filtered_documents),
            "statistics": stats,
            "filters_applied": {
                "department": department,
                "year": year,
                "supervisor": supervisor
            }
        }
        
    except Exception as e:
        print(f"Error getting supervisor-specific statistics: {e}")
        return {
            "success": False,
            "error": str(e),
            "total_documents": 0,
            "statistics": {},
            "filters_applied": {}
        }

def calculate_supervisor_specific_statistics(documents: List[Dict], supervisor: str) -> Dict[str, Any]:
    """
    Calculate statistics specifically for a supervisor's theses.
    
    :param documents: List of Elasticsearch document hits for this supervisor
    :param supervisor: The supervisor name
    :return: Dictionary containing calculated statistics
    """
    if not documents:
        return {
            "by_year": {},
            "by_department": {},
            "by_supervisor": {supervisor: 0},
            "top_keywords": {},
            "keyword_cloud_data": [],
            "year_range": {"min": None, "max": None},
            "average_abstract_length": 0,
            "supervisors_count": 1,
            "recent_theses": []
        }
    
    years = []
    departments = []
    keywords = []
    abstract_lengths = []
    all_docs = []
    
    for hit in documents:
        source = hit['_source']
        
        if source.get('year'):
            years.append(int(source['year']))
        
        if source.get('department'):
            departments.append(source['department'])
        
        keyword_field = source.get('keywords', [])
        normalized_keywords = extract_and_normalize_keywords(keyword_field)
        keywords.extend(normalized_keywords)

        abstract = source.get('abstract', '')
        if abstract:
            abstract_lengths.append(len(abstract))
        
        all_docs.append({
            'author': source.get('author', 'Unknown'),
            'year': source.get('year', 'Unknown'),
            'department': source.get('department', 'Unknown'),
            'supervisor': source.get('supervisor', []),
            'hash_code': source.get('hash_code')
        })
    
    year_counts = Counter(years)
    department_counts = Counter(departments)
    keyword_counts = Counter(keywords)

    keyword_cloud_data = [
        {"text": keyword, "value": count}
        for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:50]
    ]

    all_docs.sort(key=lambda x: int(x['year']) if x['year'] != 'Unknown' else 0, reverse=True)
    
    return {
        "by_year": dict(sorted(year_counts.items())),
        "by_department": dict(department_counts),
        "by_supervisor": {supervisor: len(documents)},
        "top_keywords": dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:15]),
        "keyword_cloud_data": keyword_cloud_data,
        "year_range": {
            "min": min(years) if years else None,
            "max": max(years) if years else None
        },
        "average_abstract_length": int(sum(abstract_lengths) / len(abstract_lengths)) if abstract_lengths else 0,
        "supervisors_count": 1,
        "recent_theses": all_docs[:20]
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
            "keyword_cloud_data": [],
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
        normalized_keywords = extract_and_normalize_keywords(keyword_field)
        keywords.extend(normalized_keywords)

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

    keyword_cloud_data = [
        {"text": keyword, "value": count}
        for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:50]
    ]

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
        "keyword_cloud_data": keyword_cloud_data,
        "year_range": {
            "min": min(years) if years else None,
            "max": max(years) if years else None
        },
        "average_abstract_length": int(sum(abstract_lengths) / len(abstract_lengths)) if abstract_lengths else 0,
        "supervisors_count": len(set(supervisors)),
        "recent_theses": recent_theses[:10]
    }

def get_unique_supervisors(es, department: str = None, year: int = None):
    """
    Get a list of unique supervisors for filter dropdown.
    
    :param es: Elasticsearch client instance
    :param department: Optional filter by department
    :param year: Optional filter by year
    :return: List of unique supervisor names
    """
    print(f"Getting supervisors for department: {department}, year: {year}")
    
    filters = []
    if department:
        filters.append({"term": {"department": department}})
    if year:
        filters.append({"term": {"year": year}})
    
    if department == "cs":
        indices = ["cs_theses"]
    elif department == "informatics":
        indices = ["infos_theses"]
    else:
        indices = ["cs_theses", "infos_theses"]
    
    print(f"Searching indices: {indices} with filters: {filters}")

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
        print(f"Found {len(supervisors)} unique supervisors for the given filters")
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
    