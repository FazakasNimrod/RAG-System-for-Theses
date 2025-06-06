# API Documentation

## Search Endpoints

### Basic Search

```
GET /search
```

Performs a keyword-based search across thesis documents with enhanced features including supervisor search and configurable result limits.

#### Parameters:

- `q`: Search query string
- `year`: (optional) Filter by year
- `sort`: (optional) Sort order by year (`asc` or `desc`, default: `desc`)
- `phrase`: (optional) Set to `true` for exact phrase search
- `department`: (optional) Filter by department (`cs` or `informatics`)
- `search_supervisors`: (optional) Set to `true` to search supervisors only
- `limit`: (optional) Number of results to return (default: `50`, max: `100`)

#### Examples:

```bash
# Basic keyword search
curl "http://127.0.0.1:5000/search?q=smart home"

# Search supervisors only
curl "http://127.0.0.1:5000/search?q=Szilágyi László&search_supervisors=true"

# Filter by department and year
curl "http://127.0.0.1:5000/search?q=neural networks&department=cs&year=2023"

# Exact phrase search with custom limit
curl "http://127.0.0.1:5000/search?q=machine learning&phrase=true&limit=25"

# Sort by year (ascending)
curl "http://127.0.0.1:5000/search?q=IoT&sort=asc"
```

### Semantic Search

```
GET /search/semantic
```

Performs vector-based semantic search to find conceptually related documents using sentence transformers.

#### Parameters:

- `q`: Search query string
- `year`: (optional) Filter by year
- `sort`: (optional) Sort order by year (`asc` or `desc`, default: `desc`)
- `limit`: (optional) Maximum number of results to return (default: `10`)
- `department`: (optional) Filter by department (`cs` or `informatics`)

#### Examples:

```bash
# Basic semantic search
curl "http://127.0.0.1:5000/search/semantic?q=neural networks architecture"

# Limit results and filter by department
curl "http://127.0.0.1:5000/search/semantic?q=smart devices&limit=20&department=cs"

# Filter by year and sort
curl "http://127.0.0.1:5000/search/semantic?q=security protocols&year=2022&sort=asc"
```

### RAG (Retrieval-Augmented Generation)

```
POST /search/rag
```

Ask questions and get AI-generated answers based on relevant documents using Ollama models with local LLM capabilities.

#### Request Body:

```json
{
  "query": "How do smart home systems integrate with IoT devices?",
  "model": "llama3.2:3b",
  "top_k": 5,
  "department": "cs"
}
```

#### Parameters:

- `query`: The question to answer
- `model`: (optional) The Ollama model to use (default: `llama3.2:3b`)
- `top_k`: (optional) Number of documents to retrieve (default: `5`)
- `department`: (optional) Filter documents by department

#### Examples:

```bash
# Basic RAG question
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the security challenges in IoT?"}'

# Specific model and department
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do neural networks process images?", "model": "llama3.1:8b", "department": "cs"}'

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

### Document Retrieval

```
GET /search/document/<hash_code>
```

Retrieve a specific document by its hash code.

#### Parameters:

- `hash_code`: 10-digit hash code identifying the document
- `department`: (optional) Filter by department for faster lookup

#### Example:

```bash
curl "http://127.0.0.1:5000/search/document/1234567890?department=cs"
```

### PDF Access

```
GET /search/pdf/<hash_code>
```

Redirect to the PDF storage service to view a PDF document.

#### Example:

```bash
curl "http://127.0.0.1:5000/search/pdf/1234567890"
# Redirects to: http://localhost:5000/1234567890
```

## Statistics Endpoints

### Get Statistics

```
GET /search/statistics
```

Get comprehensive statistics about theses with filtering support.

#### Parameters:

- `department`: (optional) Filter by department (`cs` or `informatics`)
- `year`: (optional) Filter by specific year
- `supervisor`: (optional) Get supervisor-specific statistics

#### Examples:

```bash
# General statistics
curl "http://127.0.0.1:5000/search/statistics"

# Department-specific statistics
curl "http://127.0.0.1:5000/search/statistics?department=cs"

# Supervisor-specific statistics
curl "http://127.0.0.1:5000/search/statistics?supervisor=Szilágyi László"

# Combined filters
curl "http://127.0.0.1:5000/search/statistics?department=cs&year=2023"
```

### Get Unique Supervisors

```
GET /search/statistics/supervisors
```

Get list of unique supervisors for filter dropdowns.

#### Parameters:

- `department`: (optional) Filter supervisors by department
- `year`: (optional) Filter supervisors by year

#### Example:

```bash
curl "http://127.0.0.1:5000/search/statistics/supervisors?department=cs"
```

### Get Unique Years

```
GET /search/statistics/years
```

Get list of available years for filtering.

#### Parameters:

- `department`: (optional) Filter years by department

#### Example:

```bash
curl "http://127.0.0.1:5000/search/statistics/years"
```

## Key Features

1. **Enhanced Keyword Search**:

   - Multi-field search across `abstract`, `keywords`, `author`, and `supervisor`
   - Configurable result limits (up to 100 results)
   - Supervisor-only search mode
   - Phrase search for exact matching
   - Stop word filtering for better relevance

2. **Advanced Semantic Search**:

   - Vector embeddings using SentenceTransformer models
   - Cosine similarity scoring
   - Department and year filtering
   - Configurable result limits

3. **AI-Powered Question Answering (RAG)**:

   - Local Ollama models (llama3.1:8b, llama3.2:1b, llama3.2:3b)
   - Document retrieval with relevance scoring
   - Natural language answers with source references
   - Department filtering for targeted results

4. **Comprehensive Statistics**:

   - Topic distribution analysis
   - Supervisor performance metrics
   - Year-over-year trends
   - Department comparisons
   - Interactive word clouds for keyword visualization

5. **Document Management**:

   - Hash-based document identification
   - Integration with PDF storage service
   - Direct PDF access via hash codes
   - Department-based organization

6. **Filtering & Sorting**:
   - Multi-dimensional filtering (year, department, supervisor)
   - Flexible sorting options
   - Smart conditional displays based on active filters

## Data Sources

- **CS Department**: Computer Science theses from cleaned data
- **Informatics Department**: Informatics theses with multilingual support
- **PDF Storage**: Docker-based service with hash code mapping
- **Topic Categories**: 7 main research areas with automatic classification

## Frontend Pages

- **Home/Search**: Enhanced keyword search with supervisor mode toggle
- **Semantic Search**: Vector-based conceptual search
- **Ask Questions**: RAG interface with model selection and department filtering
- **Statistics**: Comprehensive analytics with interactive visualizations
- **Sign Up/Sign In**: User authentication forms (ready for backend integration)

## Response Formats

All endpoints return JSON responses with consistent error handling and proper HTTP status codes. Search results include highlighting for matched terms and relevance scoring.
