# API Documentation

## Search Endpoints

### Basic Search

```
GET /search
```

Performs a keyword-based search across thesis documents.

#### Parameters:

- `q`: Search query string
- `year`: (optional) Filter by year
- `sort`: (optional) Sort order by year (`asc` or `desc`, default: `desc`)
- `phrase`: (optional) Set to `true` for exact phrase search

#### Examples:

```bash
# Basic keyword search
curl "http://127.0.0.1:5000/search?q=smart home"

# Filter by year
curl "http://127.0.0.1:5000/search?q=smart home&year=2023"

# Sort by year (ascending)
curl "http://127.0.0.1:5000/search?q=smart home&sort=asc"

# Exact phrase search
curl "http://127.0.0.1:5000/search?q=smart home&phrase=true"
```

### Semantic Search

```
GET /search/semantic
```

Performs vector-based semantic search to find conceptually related documents.

#### Parameters:

- `q`: Search query string
- `year`: (optional) Filter by year
- `sort`: (optional) Sort order by year (`asc` or `desc`, default: `desc`)
- `limit`: (optional) Maximum number of results to return (default: `10`)

#### Examples:

```bash
# Basic semantic search
curl "http://127.0.0.1:5000/search/semantic?q=neural networks architecture"

# Limit results
curl "http://127.0.0.1:5000/search/semantic?q=smart devices&limit=5"

# Filter by year
curl "http://127.0.0.1:5000/search/semantic?q=security protocols&year=2022"
```

### RAG (Retrieval-Augmented Generation)

```
POST /search/rag
```

Ask questions and get AI-generated answers based on relevant documents using Ollama models.

#### Request Body:

```json
{
  "query": "How do smart home systems integrate with IoT devices?",
  "model": "llama3.2:3b",
  "top_k": 5
}
```

#### Parameters:

- `query`: The question to answer
- `model`: (optional) The Ollama model to use (default: `llama3.2:3b`)
- `top_k`: (optional) Number of documents to retrieve (default: `5`)

#### Examples:

```bash
# Basic RAG question
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the security challenges in IoT?"}'

# Specific model
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do neural networks process images?", "model": "llama3.1:8b"}'

# Custom document count
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain blockchain technology", "top_k": 8}'
```

### Available RAG Models

```
GET /search/models
```

Get a list of available Ollama models for RAG.

#### Example:

```bash
curl "http://127.0.0.1:5000/search/models"
```

## Key Features

1. **Keyword Search**:

   - Searches across `abstract`, `keywords`, and `author`
   - Supports highlighting of matches
   - Provides phrase search option for exact matching

2. **Semantic Search**:

   - Uses vector embeddings for conceptual similarity
   - Returns documents based on meaning, not just keywords
   - Adjustable result limit

3. **AI-Powered Question Answering (RAG)**:

   - Uses local Ollama models (llama3.1:8b, llama3.2:1b, llama3.2:3b)
   - Retrieves relevant documents and generates answers
   - Returns both the answer and source references

4. **Filtering & Sorting**:

   - Year filtering across all search types
   - Sorting options for traditional searches
   - Relevance ranking in semantic search

5. **Result Highlighting**:
   - Highlights matching terms in abstracts and keywords
   - Expandable abstracts with preserved highlighting

## Frontend Pages

- **Home/Search**: Traditional keyword search with phrase option
- **Semantic Search**: Meaning-based document retrieval
- **Ask Questions**: RAG interface with model selection
- **Sign Up/Sign In**: User authentication forms
