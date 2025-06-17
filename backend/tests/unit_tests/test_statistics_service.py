import pytest
import sys
import os
from unittest.mock import Mock, patch
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'app'))

from statistics_service import (
    get_statistics,
    get_unique_supervisors,
    get_unique_years,
    calculate_document_statistics,
    extract_and_normalize_keywords,
    normalize_keyword
)


class TestStatisticsService:
    """Test cases for statistics service functions"""
    
    @pytest.fixture
    def mock_es(self):
        """Mock Elasticsearch instance"""
        return Mock()
    
    @pytest.fixture
    def sample_documents(self):
        """Sample Elasticsearch documents for testing"""
        return [
            {
                '_source': {
                    'author': 'Gáll János',
                    'supervisor': 'Bakó László',
                    'year': 2023,
                    'department': 'cs',
                    'keywords': ['machine learning', 'ai'],
                    'abstract': 'This is a test abstract about machine learning and neural networks.',
                    'hash_code': 123456
                }
            },
            {
                '_source': {
                    'author': 'Hammas Attila',
                    'supervisor': ['Brassai Sándor Tihamér', 'Antal Margit'],
                    'year': 2022,
                    'department': 'informatics',
                    'keywords': 'data mining, algorithm, deep learning',
                    'abstract': 'Another test abstract about data science.',
                    'hash_code': 789012
                }
            },
            {
                '_source': {
                    'author': 'Bálint Adolf',
                    'supervisor': 'Lefkovits László, Kátai Zoltán',
                    'year': 2023,
                    'department': 'cs',
                    'keywords': ['web development', 'javascript'],
                    'abstract': 'Web development thesis abstract.',
                    'hash_code': 456789
                }
            }
        ]
    
    def test_normalize_keyword_basic(self):
        """Test basic keyword normalization"""
        assert normalize_keyword('machine learning') == 'Machine Learning'
        assert normalize_keyword('MACHINE LEARNING') == 'Machine Learning'
        assert normalize_keyword('machine-learning') == 'Machine Learning'
        assert normalize_keyword('') == ''
    
    def test_normalize_keyword_special_cases(self):
        """Test special keyword mappings"""
        assert normalize_keyword('ai') == 'Artificial Intelligence'
        assert normalize_keyword('iot') == 'IoT'
        assert normalize_keyword('javascript') == 'JavaScript'
        assert normalize_keyword('web app') == 'Web Application'
        assert normalize_keyword('spring boot') == 'Spring Boot'
    
    def test_extract_and_normalize_keywords_list(self):
        """Test keyword extraction from list format"""
        keywords = ['machine learning', 'AI', 'deep learning']
        result = extract_and_normalize_keywords(keywords)
        
        assert 'Machine Learning' in result
        assert 'Artificial Intelligence' in result
        assert 'Deep Learning' in result
        assert len(result) == 3
    
    def test_extract_and_normalize_keywords_string(self):
        """Test keyword extraction from comma-separated string"""
        keywords = 'machine learning, AI, deep learning'
        result = extract_and_normalize_keywords(keywords)
        
        assert 'Machine Learning' in result
        assert 'Artificial Intelligence' in result
        assert 'Deep Learning' in result
        assert len(result) == 3
    
    def test_extract_and_normalize_keywords_empty(self):
        """Test keyword extraction with empty/null input"""
        assert extract_and_normalize_keywords([]) == []
        assert extract_and_normalize_keywords('') == []
        assert extract_and_normalize_keywords(None) == []
    
    def test_calculate_document_statistics_basic(self, sample_documents):
        """Test basic document statistics calculation"""
        stats = calculate_document_statistics(sample_documents)
        
        assert stats['by_year'] == {2022: 1, 2023: 2}
        
        assert stats['by_department'] == {'cs': 2, 'informatics': 1}
        
        expected_supervisors = {'Bakó László', 'Brassai Sándor Tihamér', 'Antal Margit', 'Lefkovits László', 'Kátai Zoltán'}
        assert stats['supervisors_count'] == len(expected_supervisors)
        
        assert len(stats['recent_theses']) == 3
        
        assert stats['year_range']['min'] == 2022
        assert stats['year_range']['max'] == 2023
    
    def test_calculate_document_statistics_empty(self):
        """Test statistics calculation with empty document list"""
        stats = calculate_document_statistics([])
        
        assert stats['by_year'] == {}
        assert stats['by_department'] == {}
        assert stats['by_supervisor'] == {}
        assert stats['top_keywords'] == {}
        assert stats['year_range']['min'] is None
        assert stats['year_range']['max'] is None
        assert stats['supervisors_count'] == 0
        assert stats['recent_theses'] == []
        assert stats['average_abstract_length'] == 0
    
    def test_supervisor_field_handling(self):
        """Test different supervisor field formats"""
        documents = [
            {'_source': {'supervisor': 'Antal Margit', 'year': 2023, 'department': 'cs', 'abstract': 'test'}},
            {'_source': {'supervisor': ['Bakó László', 'Brassai Sándor Tihamér'], 'year': 2023, 'department': 'cs', 'abstract': 'test'}},
            {'_source': {'supervisor': 'Lefkovits László, Kátai Zoltán', 'year': 2023, 'department': 'cs', 'abstract': 'test'}},
        ]
        
        stats = calculate_document_statistics(documents)
        
        expected_supervisors = {'Antal Margit', 'Bakó László', 'Brassai Sándor Tihamér', 'Lefkovits László', 'Kátai Zoltán'}
        assert stats['supervisors_count'] == len(expected_supervisors)
    
    def test_keyword_processing(self, sample_documents):
        """Test keyword processing and cloud data generation"""
        stats = calculate_document_statistics(sample_documents)
        
        assert 'top_keywords' in stats
        assert 'keyword_cloud_data' in stats
        
        assert len(stats['top_keywords']) > 0
        assert isinstance(stats['keyword_cloud_data'], list)
        
        if stats['keyword_cloud_data']:
            keyword_item = stats['keyword_cloud_data'][0]
            assert 'text' in keyword_item
            assert 'value' in keyword_item
    
    def test_abstract_length_calculation(self, sample_documents):
        """Test average abstract length calculation"""
        stats = calculate_document_statistics(sample_documents)
        
        abstracts = [doc['_source']['abstract'] for doc in sample_documents]
        expected_avg = sum(len(abstract) for abstract in abstracts) / len(abstracts)
        
        assert stats['average_abstract_length'] == int(expected_avg)
    
    def test_get_statistics_no_filters(self, mock_es, sample_documents):
        """Test get_statistics without any filters"""
        mock_es.search.return_value = {
            'hits': {'hits': sample_documents}
        }
        
        result = get_statistics(mock_es)
        
        assert result['success'] is True
        assert result['total_documents'] == 3
        assert 'statistics' in result
        assert result['filters_applied'] == {
            'department': None,
            'year': None,
            'supervisor': None
        }
        
        mock_es.search.assert_called_once()
        call_args = mock_es.search.call_args
        assert 'cs_theses,infos_theses' in call_args[1]['index']
    
    def test_get_statistics_with_department_filter(self, mock_es, sample_documents):
        """Test get_statistics with department filter"""
        mock_es.search.return_value = {
            'hits': {'hits': sample_documents[:2]}
        }
        
        result = get_statistics(mock_es, department='cs')
        
        assert result['success'] is True
        assert result['total_documents'] == 2
        assert result['filters_applied']['department'] == 'cs'
        
        call_args = mock_es.search.call_args
        assert call_args[1]['index'] == 'cs_theses'
        
        query = call_args[1]['body']['query']
        assert 'bool' in query
        assert 'filter' in query['bool']
    
    def test_get_statistics_with_year_filter(self, mock_es, sample_documents):
        """Test get_statistics with year filter"""
        mock_es.search.return_value = {
            'hits': {'hits': [sample_documents[0], sample_documents[2]]}
        }
        
        result = get_statistics(mock_es, year=2023)
        
        assert result['success'] is True
        assert result['filters_applied']['year'] == 2023
        
        call_args = mock_es.search.call_args
        filters = call_args[1]['body']['query']['bool']['filter']
        year_filter = next((f for f in filters if 'year' in f.get('term', {})), None)
        assert year_filter is not None
        assert year_filter['term']['year'] == 2023
    
    def test_get_statistics_elasticsearch_error(self, mock_es):
        """Test get_statistics error handling"""
        mock_es.search.side_effect = Exception("Elasticsearch connection failed")
        
        result = get_statistics(mock_es)
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Elasticsearch connection failed' in result['error']
        assert result['total_documents'] == 0
    
    def test_get_unique_supervisors_no_filters(self, mock_es):
        """Test get_unique_supervisors without filters"""
        mock_es.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'supervisor': 'Antal Margit'}},
                    {'_source': {'supervisor': ['Bakó László', 'Brassai Sándor Tihamér']}},
                    {'_source': {'supervisor': 'Lefkovits László, Kátai Zoltán'}},
                ]
            }
        }
        
        result = get_unique_supervisors(mock_es)
        
        expected_supervisors = ['Antal Margit', 'Bakó László', 'Brassai Sándor Tihamér', 'Lefkovits László, Kátai Zoltán']
        assert sorted(result) == sorted(expected_supervisors)
        
        call_args = mock_es.search.call_args
        assert call_args[1]['body']['query'] == {'match_all': {}}
    
    def test_get_unique_supervisors_with_filters(self, mock_es):
        """Test get_unique_supervisors with department and year filters"""
        mock_es.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'supervisor': 'Antal Margit'}},
                    {'_source': {'supervisor': 'Bakó László'}},
                ]
            }
        }
        
        result = get_unique_supervisors(mock_es, department='cs', year=2023)
        
        assert len(result) == 2
        assert 'Bakó László' in result
        assert 'Antal Margit' in result
        
        call_args = mock_es.search.call_args
        filters = call_args[1]['body']['query']['bool']['filter']
        assert len(filters) == 2
    
    def test_get_unique_years_no_filters(self, mock_es):
        """Test get_unique_years without filters"""
        mock_es.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'year': 2023}},
                    {'_source': {'year': 2022}},
                    {'_source': {'year': 2021}},
                    {'_source': {'year': 2023}},
                ]
            }
        }
        
        result = get_unique_years(mock_es)
        
        assert result == [2023, 2022, 2021]
        
        call_args = mock_es.search.call_args
        assert call_args[1]['body']['query'] == {'match_all': {}}
        assert call_args[1]['body']['_source'] == ['year']
    
    def test_get_unique_years_with_department_filter(self, mock_es):
        """Test get_unique_years with department filter"""
        mock_es.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'year': 2023}},
                    {'_source': {'year': 2022}}
                ]
            }
        }
        
        result = get_unique_years(mock_es, department='cs')
        
        assert result == [2023, 2022]
        
        call_args = mock_es.search.call_args
        assert call_args[1]['index'] == 'cs_theses'
        assert 'filter' in call_args[1]['body']['query']['bool']
    
    def test_get_unique_years_error_handling(self, mock_es):
        """Test get_unique_years error handling"""
        mock_es.search.side_effect = Exception("Aggregation failed")
        
        result = get_unique_years(mock_es)
        
        assert result == []
    
    def test_supervisor_specific_statistics(self, mock_es):
        """Test statistics for a specific supervisor"""
        supervisor_docs = [
            {
                '_source': {
                    'author': 'Gáll János',
                    'supervisor': 'Bakó László',
                    'year': 2023,
                    'department': 'cs',
                    'keywords': ['ai', 'machine learning'],
                    'abstract': 'AI research thesis.',
                    'hash_code': 111
                }
            },
            {
                '_source': {
                    'author': 'Hammas Attila',
                    'supervisor': ['Bakó László', 'Antal Margit'],
                    'year': 2022,
                    'department': 'cs',
                    'keywords': ['deep learning'],
                    'abstract': 'Deep learning thesis.',
                    'hash_code': 222
                }
            }
        ]
        
        mock_es.search.return_value = {
            'hits': {'hits': supervisor_docs}
        }
        
        result = get_statistics(mock_es, supervisor='Bakó László')
        
        assert result['success'] is True
        assert result['filters_applied']['supervisor'] == 'Bakó László'
        assert result['total_documents'] == 2
    
    def test_malformed_supervisor_field(self):
        """Test handling of malformed supervisor fields"""
        documents = [
            {'_source': {'supervisor': '', 'year': 2023, 'department': 'cs'}},
            {'_source': {'supervisor': None, 'year': 2023, 'department': 'cs'}},
            {'_source': {'supervisor': [], 'year': 2023, 'department': 'cs'}},
            {'_source': {'year': 2023, 'department': 'cs'}},
        ]
        
        stats = calculate_document_statistics(documents)
        
        assert stats['supervisors_count'] == 0
        assert stats['by_supervisor'] == {}
    
    def test_malformed_keywords_field(self):
        """Test handling of malformed keywords fields"""
        documents = [
            {'_source': {'keywords': '', 'year': 2023, 'department': 'cs'}},
            {'_source': {'keywords': None, 'year': 2023, 'department': 'cs'}},
            {'_source': {'keywords': [], 'year': 2023, 'department': 'cs'}},
            {'_source': {'year': 2023, 'department': 'cs'}},
        ]
        
        stats = calculate_document_statistics(documents)
        
        assert stats['top_keywords'] == {}
        assert stats['keyword_cloud_data'] == []
    
    def test_missing_year_field(self):
        """Test handling of documents without year field"""
        documents = [
            {'_source': {'department': 'cs', 'supervisor': 'Antal Margit'}},
            {'_source': {'department': 'cs', 'supervisor': 'Bakó László', 'year': 2023}},
        ]
        
        stats = calculate_document_statistics(documents)
        
        assert stats['by_year'] == {2023: 1}
        assert stats['year_range']['min'] == 2023
        assert stats['year_range']['max'] == 2023
        
        assert len(stats['recent_theses']) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
