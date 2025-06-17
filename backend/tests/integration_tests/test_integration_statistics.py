import pytest
import json
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'app'))

from app import app


class TestStatisticsIntegration:
    """Integration tests for statistics API endpoints and services"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        return app.test_client()
    
    @pytest.fixture
    def sample_statistics_response(self):
        """Sample statistics response that would come from the service"""
        return {
            "success": True,
            "total_documents": 4,
            "statistics": {
                "by_year": {"2021": 1, "2023": 2, "2024": 1},
                "by_department": {"cs": 3, "informatics": 1},
                "by_supervisor": {"Bakó László": 1, "Brassai Sándor Tihamér": 1, "Lefkovits László": 1, "Antal Margit": 1},
                "top_keywords": {"FPGA": 2, "machine learning": 1, "image processing": 1},
                "supervisors_count": 4,
                "year_range": {"min": 2021, "max": 2024},
                "average_abstract_length": 85,
                "recent_theses": []
            },
            "filters_applied": {
                "department": None,
                "year": None,
                "supervisor": None
            }
        }
    
    def test_statistics_endpoint_integration_no_filters(self, client, sample_statistics_response):
        """Test full integration: API endpoint → routes → service → statistics calculation"""
        with patch('routes.get_statistics') as mock_get_stats:
            mock_get_stats.return_value = sample_statistics_response
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics')
                
                assert response.status_code == 200
                assert response.is_json
                
                data = response.get_json()
                
                assert 'success' in data
                assert data['success'] is True
                assert 'total_documents' in data
                assert 'statistics' in data
                assert 'filters_applied' in data
                
                stats = data['statistics']
                assert 'by_year' in stats
                assert 'by_department' in stats
                assert 'by_supervisor' in stats
                assert 'supervisors_count' in stats
                
                assert data['total_documents'] == 4
                assert stats['by_year'] == {"2021": 1, "2023": 2, "2024": 1} 
                assert stats['by_department'] == {'cs': 3, 'informatics': 1}
                assert stats['supervisors_count'] == 4
                
                assert data['filters_applied'] == {
                    'department': None,
                    'year': None,
                    'supervisor': None
                }
                
                mock_get_stats.assert_called_once_with(mock_es, None, None, None)
    
    def test_statistics_endpoint_with_department_filter_integration(self, client):
        """Test integration with department filter: API → routes → service with filtering"""
        filtered_response = {
            "success": True,
            "total_documents": 3,
            "statistics": {
                "by_year": {"2021": 1, "2023": 2},
                "by_department": {"cs": 3},
                "by_supervisor": {"Bakó László": 1, "Brassai Sándor Tihamér": 1, "Lefkovits László": 1},
                "supervisors_count": 3
            },
            "filters_applied": {
                "department": "cs",
                "year": None,
                "supervisor": None
            }
        }
        
        with patch('routes.get_statistics') as mock_get_stats:
            mock_get_stats.return_value = filtered_response
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics?department=cs')
                
                assert response.status_code == 200
                data = response.get_json()
                
                assert data['success'] is True
                assert data['filters_applied']['department'] == 'cs'
                assert data['total_documents'] == 3
                
                stats = data['statistics']
                assert stats['by_department'] == {'cs': 3}
                assert 'informatics' not in stats['by_department']
                
                mock_get_stats.assert_called_once_with(mock_es, 'cs', None, None)
    
    def test_statistics_endpoint_with_year_filter_integration(self, client):
        """Test integration with year filter affecting both routes and service layers"""
        year_filtered_response = {
            "success": True,
            "total_documents": 2,
            "statistics": {
                "by_year": {"2023": 2},
                "by_department": {"cs": 2},
                "supervisors_count": 2
            },
            "filters_applied": {
                "department": None,
                "year": 2023,
                "supervisor": None
            }
        }
        
        with patch('routes.get_statistics') as mock_get_stats:
            mock_get_stats.return_value = year_filtered_response
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics?year=2023')
                
                assert response.status_code == 200
                data = response.get_json()
                
                assert data['success'] is True
                assert data['filters_applied']['year'] == 2023
                assert data['total_documents'] == 2
                
                stats = data['statistics']
                assert stats['by_year'] == {"2023": 2}
                
                mock_get_stats.assert_called_once_with(mock_es, None, 2023, None)
    
    def test_supervisors_endpoint_integration(self, client):
        """Test supervisors endpoint integration: API → routes → service → supervisor extraction"""
        with patch('routes.get_unique_supervisors') as mock_get_supervisors:
            mock_get_supervisors.return_value = [
                'Antal Margit', 'Bakó László', 'Brassai Sándor Tihamér', 
                'Kátai Zoltán', 'Lefkovits László', 'Szilágyi László'
            ]
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics/supervisors')
                
                assert response.status_code == 200
                assert response.is_json
                
                supervisors = response.get_json()
                assert isinstance(supervisors, list)
                assert len(supervisors) == 6
                
                expected_supervisors = ['Antal Margit', 'Bakó László', 'Brassai Sándor Tihamér', 'Lefkovits László']
                for supervisor in expected_supervisors:
                    assert supervisor in supervisors
                
                assert supervisors == sorted(supervisors)
                
                mock_get_supervisors.assert_called_once_with(mock_es, None, None)
    
    def test_supervisors_endpoint_with_filters_integration(self, client):
        """Test supervisors endpoint with department and year filters"""
        with patch('routes.get_unique_supervisors') as mock_get_supervisors:
            mock_get_supervisors.return_value = ['Bakó László', 'Lefkovits László']
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics/supervisors?department=cs&year=2023')
                
                assert response.status_code == 200
                supervisors = response.get_json()
                assert len(supervisors) == 2
                assert 'Bakó László' in supervisors
                assert 'Lefkovits László' in supervisors
                
                mock_get_supervisors.assert_called_once_with(mock_es, 'cs', 2023)
    
    def test_years_endpoint_integration(self, client):
        """Test years endpoint integration: API → routes → service → year extraction"""
        with patch('routes.get_unique_years') as mock_get_years:
            mock_get_years.return_value = [2024, 2023, 2022, 2021]
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics/years')
                
                assert response.status_code == 200
                assert response.is_json
                
                years = response.get_json()
                assert isinstance(years, list)
                assert len(years) == 4
                
                expected_years = [2024, 2023, 2022, 2021]
                assert years == expected_years
                
                mock_get_years.assert_called_once_with(mock_es, None)
    
    def test_years_endpoint_with_department_filter_integration(self, client):
        """Test years endpoint with department filter"""
        with patch('routes.get_unique_years') as mock_get_years:
            mock_get_years.return_value = [2023, 2021]
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics/years?department=cs')
                
                assert response.status_code == 200
                years = response.get_json()
                assert years == [2023, 2021]
                
                mock_get_years.assert_called_once_with(mock_es, 'cs')
    
    def test_error_handling_integration(self, client):
        """Test error handling integration: Elasticsearch failure → service → routes → API response"""
        with patch('routes.get_statistics') as mock_get_stats:
            mock_get_stats.side_effect = Exception("Elasticsearch connection failed")
            
            with patch('routes.getattr') as mock_getattr:
                mock_es = Mock()
                mock_getattr.return_value = mock_es
                
                response = client.get('/search/statistics')
                
                assert response.status_code == 500
                data = response.get_json()
                
                assert 'error' in data
                assert 'Statistics failed' in data['error']
                assert 'Elasticsearch connection failed' in data['error']
    
    def test_no_elasticsearch_connection_integration(self, client):
        """Test integration when Elasticsearch is not available"""
        with patch('routes.getattr') as mock_getattr:
            mock_getattr.return_value = None
            
            response = client.get('/search/statistics')
            
            assert response.status_code == 500
            data = response.get_json()
            
            assert 'error' in data
            assert 'Elasticsearch connection is not available' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
