# System Architecture

## Overview

This document outlines the architecture of the thesis search and retrieval system. The application follows a client-server architecture with a React frontend, Flask backend, Elasticsearch for search functionality, and Ollama for local LLM capabilities.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│             │      │              │      │                 │
│  React      │◄────►│  Flask       │◄────►│  Elasticsearch  │
│  Frontend   │      │  Backend     │      │  Search Engine  │
│             │      │              │      │                 │
└─────────────┘      └──────┬───────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │              │
                     │  Ollama      │
                     │  LLM Service │
                     │              │
                     └──────────────┘
```

## Components

### 1. Frontend (React)

The frontend is built using React and provides multiple search interfaces:

#### Pages

- **Search Page**: Standard keyword search with phrase search capability
- **Semantic Search Page**: Vector-based semantic search
- **RAG Page**: Question answering with document references
- **Sign Up/Sign In Pages**: User authentication forms

#### Key Components

- **SearchBar**: Input field for queries
- **ResultsList**: Displays search results with highlighting
- **Sidebar**: Filters and options for search
- **RagPage**: Interface for asking questions

#### Services

- **elasticsearchService.js**: Handles API calls for basic and semantic search
- **ragService.js**: Manages communication with the RAG API endpoints

### 2. Backend (Flask)

The backend is built with Flask and serves as an API layer between the frontend and the search infrastructure.

#### Routes

- **/search/**: Basic keyword and phrase search
- **/search/semantic**: Vector-based semantic search
- **/search/rag**: Question answering using retrieved documents
- **/search/models**: Available LLM models for RAG

#### Services

- **services.py**: Core search functionality implementation
- **ollama_rag_service.py**: Integration with Ollama for RAG

### 3. Elasticsearch

Provides the search engine capabilities for the application.

#### Indices

- **cs_theses**: Primary index for keyword and phrase searches
- **cs_theses_semantic**: Index with vector embeddings for semantic search

#### Features Used

- Text search with highlighting
- Filter and sort capabilities
- Vector search using script_score queries

### 4. Ollama

Local large language model service for generating answers in the RAG system.

#### Models

- **llama3.1:8b**: 8B parameter model for high-quality answers
- **llama3.2:1b**: 1B parameter model for faster responses
- **llama3.2:3b**: 3B parameter model balanced for quality and speed

## Data Flow

### 1. Document Indexing

```
PDF Documents → Extraction → JSON Data → Index Creation → Elasticsearch
```

### 2. Basic Search

```
User Query → Frontend → Backend API → Elasticsearch Query → Results → Frontend Display
```

### 3. Semantic Search

```
User Query → Frontend → Backend API → Vector Embedding → Vector Search → Results → Frontend Display
```

### 4. RAG Question Answering

```
User Question → Frontend → Backend API → Document Retrieval → Context Building →
Ollama LLM → Generated Answer → Results with References → Frontend Display
```

## Technical Details

### API Communication

- REST API between frontend and backend
- JSON data format for requests and responses
- Axios for frontend HTTP requests

### Search Implementation

- Keyword search: Multi-match queries across fields
- Phrase search: Match phrase queries for exact matching
- Semantic search: Cosine similarity between vector embeddings
- Query highlighting: Returns highlighted text fragments

### Vector Embeddings

- SentenceTransformer model ('all-MiniLM-L6-v2')
- 384-dimension embeddings stored in Elasticsearch
- Cosine similarity for vector matching

### RAG Implementation

- Retrieved document context passed to Ollama API
- Custom prompt template for answer generation
- Response streaming disabled for direct answers
- References returned with relevance scores

## Security & Performance

### Security

- Environment variables for sensitive configuration
- Cross-origin resource sharing (CORS) enabled for frontend
- Input validation in API endpoints

### Performance Optimizations

- Elasticsearch field boosting for relevance
- Optimized vector search queries
- Adjustable result limits and document counts
- Model caching in Ollama

## Deployment Considerations

### Requirements

- Python 3.8+
- Node.js 14+
- Elasticsearch 7.x or 8.x
- Ollama with required models

### Environment Setup

- `.env` file for configuration
- Separate development and production settings
- Elasticsearch connection details
- Ollama API base URL

## Future Extensions

1. **Authentication Backend**: Implement the backend for user authentication
2. **Personalized Search**: Save user search history and preferences
3. **Advanced Filtering**: Add more filter options beyond year
4. **Model Fine-tuning**: Fine-tune LLMs on specific thesis domains
5. **Real-time Chat**: Add conversational interface with context memory
