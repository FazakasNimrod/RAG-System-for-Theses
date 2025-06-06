# System Architecture

## Overview

This document outlines the architecture of the comprehensive thesis search and retrieval system. The application follows a modern client-server architecture with React frontend, Flask backend, Elasticsearch for search functionality, Ollama for local LLM capabilities, and a Docker-based PDF storage service with hash-code identification.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│             │      │              │      │                 │
│  React      │◄────►│  Flask       │◄────►│  Elasticsearch  │
│  Frontend   │      │  Backend     │      │  Search Engine  │
│             │      │              │      │                 │
└─────────────┘      └──────┬───────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐      ┌─────────────────┐
                     │              │      │                 │
                     │  Ollama      │      │  PDF Storage    │
                     │  LLM Service │      │  Docker Service │
                     │              │      │                 │
                     └──────────────┘      └─────────────────┘
```

## Components

### 1. Frontend (React)

The frontend provides multiple specialized interfaces for different search paradigms and user needs.

#### Pages

- **Search Page**: Enhanced keyword search with supervisor mode toggle

  - Dynamic search behavior (theses vs supervisors)
  - Intuitive search mode switching
  - Advanced filtering sidebar
  - Configurable result limits (up to 100)

- **Semantic Search Page**: Vector-based conceptual search

  - Sentence transformer embeddings
  - Similarity-based ranking
  - Department filtering
  - Adjustable result limits

- **RAG Page**: AI-powered question answering

  - Natural language question interface
  - Model selection (3 Ollama models)
  - Document count configuration
  - Department filtering for targeted results

- **Statistics Page**: Comprehensive analytics dashboard

  - Interactive topic distribution pie charts
  - Top supervisors analysis
  - Year-over-year trends
  - Keyword visualization with word clouds
  - Smart conditional displays based on filters

- **Authentication Pages**: User registration and login forms

#### Key Components

- **SearchBar**: Enhanced with search mode toggle and dynamic placeholders
- **ResultsList**: Displays search results with highlighting and PDF access
- **TopicPieChart**: Interactive visualization of research topic distribution
- **StatisticsSidebar**: Dynamic filtering with cascading dropdowns
- **StatisticsDisplay**: Comprehensive analytics with responsive layouts
- **WordCloud**: Interactive keyword visualization

#### Services

- **elasticsearchService.js**: Enhanced API calls with configurable limits
- **ragService.js**: RAG functionality with model selection
- **statisticsService.js**: Statistics API integration

### 2. Backend (Flask)

The backend serves as a comprehensive API layer with multiple specialized services.

#### Enhanced Routes

- **/search/**: Multi-mode search (keyword, phrase, supervisor)

  - Configurable result limits (default: 50, max: 100)
  - Advanced filtering and sorting
  - Stop word processing
  - Department-based indexing

- **/search/semantic**: Vector similarity search

  - Cosine similarity scoring
  - Embedding-based retrieval
  - Performance optimized queries

- **/search/rag**: AI question answering

  - Document retrieval with relevance ranking
  - Ollama model integration
  - Context-aware answer generation

- **/search/statistics**: Comprehensive analytics

  - Real-time aggregations
  - Multi-dimensional filtering
  - Supervisor-specific insights

- **/search/models**: Available LLM models
- **/search/document/<hash_code>**: Direct document access
- **/search/pdf/<hash_code>**: PDF storage integration

#### Services

- **services.py**: Enhanced search functionality with configurable limits
- **ollama_rag_service.py**: Advanced RAG with document scoring
- **statistics_service.py**: Comprehensive analytics with keyword normalization
- **stop_words.py**: Multi-language stop word filtering

### 3. Elasticsearch

Provides the core search engine capabilities with multiple specialized indices.

#### Indices

- **cs_theses**: Computer Science department regular search
- **cs_theses_semantic**: CS department with vector embeddings
- **infos_theses**: Informatics department regular search
- **infos_theses_semantic**: Informatics department with vector embeddings

#### Features Used

- **Multi-field search**: Abstract, keywords, author, supervisor
- **Vector search**: Dense vector similarity with cosine scoring
- **Highlighting**: Term highlighting in abstracts and keywords
- **Aggregations**: Statistics and analytics queries
- **Filtering**: Department, year, and supervisor filtering

### 4. Ollama

Local large language model service providing AI-powered question answering.

#### Available Models

- **llama3.1:8b**: High-quality responses, slower processing
- **llama3.2:1b**: Fastest responses, good for simple questions
- **llama3.2:3b**: Balanced performance and quality (default)

#### Features

- **Local processing**: No external API dependencies
- **Context-aware**: Uses retrieved documents for grounding
- **Configurable**: Temperature, top_p, and length controls
- **Department filtering**: Targeted document retrieval

### 5. PDF Storage Service

Docker-based service for PDF document management with hash-code identification.

#### Features

- **Hash-based identification**: 10-digit unique codes for each PDF
- **Department organization**: Separate folders for CS and Informatics
- **Direct access**: RESTful API for PDF retrieval
- **Metadata storage**: PostgreSQL backend for file information

## Data Flow

### 1. Document Processing and Indexing

```
PDF Documents → Text Extraction → Topic Classification → Hash Code Generation →
Index Creation → Elasticsearch Storage
```

#### Topic Classification Pipeline

```
PDF Content → LLM Analysis → Research Category Assignment →
7-Category Classification → Statistics Integration
```

### 2. Search Operations

#### Basic Search Flow

```
User Query → Search Mode Detection → Stop Word Filtering →
Elasticsearch Query → Result Ranking → Highlighting → Frontend Display
```

#### Semantic Search Flow

```
User Query → Vector Embedding → Similarity Search →
Cosine Scoring → Result Ranking → Frontend Display
```

#### RAG Question Answering Flow

```
User Question → Document Retrieval → Context Building →
Ollama Processing → Answer Generation → Reference Extraction → Frontend Display
```

### 3. Statistics Generation

```
Filter Selection → Multi-Index Aggregation → Real-time Computation →
Visualization Data → Interactive Charts → User Interface
```

## Technical Implementation

### API Communication

- **RESTful design**: Standard HTTP methods and status codes
- **JSON data format**: Consistent request/response structure
- **Error handling**: Comprehensive error messages and fallbacks
- **CORS enabled**: Cross-origin requests for development

### Search Implementation

- **Multi-index queries**: Simultaneous search across departments
- **Relevance tuning**: Field boosting and minimum match thresholds
- **Performance optimization**: Efficient query structures and caching
- **Result limiting**: Configurable limits with performance considerations

### Vector Embeddings

- **SentenceTransformer**: 'all-MiniLM-L6-v2' model for consistency
- **384-dimensional vectors**: Stored as dense vectors in Elasticsearch
- **Cosine similarity**: Mathematical similarity scoring
- **Index optimization**: Proper vector field configuration

### RAG Implementation

- **Document scoring**: Relevance-based document selection
- **Context optimization**: Optimal context length for model processing
- **Prompt engineering**: Structured prompts for consistent responses
- **Reference tracking**: Maintains source document relationships

### Statistics Engine

- **Real-time aggregations**: Dynamic statistics based on current filters
- **Keyword normalization**: Intelligent keyword grouping and cleaning
- **Multi-dimensional analysis**: Department, year, supervisor cross-analysis
- **Visualization optimization**: Data prepared for chart libraries

## Security & Performance

### Security Measures

- **Input validation**: Query sanitization and parameter checking
- **Rate limiting**: Implicit through result limits and timeouts
- **Error handling**: Secure error messages without information leakage
- **Environment configuration**: Sensitive data in environment variables

### Performance Optimizations

- **Index optimization**: Proper field mapping and analysis
- **Query efficiency**: Optimized Elasticsearch queries
- **Result limiting**: Configurable limits to prevent overload
- **Caching strategies**: Model caching in Ollama service
- **Responsive design**: Efficient frontend rendering

## Deployment Architecture

### Development Setup

- **Local Elasticsearch**: Single-node development cluster
- **Local Ollama**: CPU-based model serving
- **Flask development server**: Debug mode enabled
- **React development server**: Hot reload enabled
- **Docker Compose**: PDF storage service

### Production Considerations

- **Elasticsearch cluster**: Multi-node setup for scalability
- **Ollama scaling**: GPU acceleration for better performance
- **Web server**: Production WSGI server (Gunicorn)
- **Static serving**: Optimized static file delivery
- **Load balancing**: Multiple backend instances
- **Monitoring**: Application and infrastructure monitoring

## Data Organization

### Document Structure

```json
{
  "author": "Author Name",
  "year": 2023,
  "department": "cs",
  "supervisor": ["Supervisor Name"],
  "abstract": "Research abstract text",
  "keywords": ["keyword1", "keyword2"],
  "hash_code": 1234567890,
  "abstract_vector": [0.1, 0.2, ...] // For semantic indices
}
```

### Topic Categories

1. **Artificial Intelligence & Machine Learning**
2. **Web & Mobile Application Development**
3. **IoT, Embedded Systems & Hardware**
4. **Healthcare & Bioinformatics**
5. **Education Technology & Gamification**
6. **Security & Network Systems**
7. **Business & Management Systems**

## Future Extensions

### Planned Enhancements

1. **User Authentication Backend**: Complete user management system
2. **Advanced Analytics**: Machine learning insights and trends
3. **Real-time Collaboration**: Shared research spaces
4. **API Rate Limiting**: Formal rate limiting implementation
5. **Caching Layer**: Redis-based caching for improved performance
6. **Full-text Search**: PDF content indexing beyond metadata
7. **Recommendation Engine**: Personalized thesis recommendations
8. **Export Functionality**: CSV, PDF report generation
9. **Advanced Visualizations**: Interactive timeline and network graphs
10. **Multi-language Support**: Extended language capabilities

### Scalability Considerations

- **Microservices**: Service decomposition for independent scaling
- **Container orchestration**: Kubernetes deployment
- **Database sharding**: Elasticsearch index distribution
- **CDN integration**: Global content delivery
- **Auto-scaling**: Dynamic resource allocation based on load
