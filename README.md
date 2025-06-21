# **ThesisFinder: Intelligent Search in Academic Theses**

## **Project Overview**

ThesisFinder is a comprehensive full-stack solution for searching, analyzing, and interacting with academic theses. Built with a powerful combination of traditional search, semantic search, and AI-powered question answering capabilities, it enables researchers to find information more effectively through multiple search paradigms. The system combines modern web technologies with advanced AI to create an intuitive platform for academic research discovery.

### **Key Features**

- **Traditional Search**: Full-text search with keyword highlighting and stop word handling
- **Phrase Search**: Exact phrase matching for precise queries
- **Semantic Search**: Vector-based semantic similarity search using SentenceTransformers
- **AI-Powered Question Answering**: RAG (Retrieval-Augmented Generation) system with multiple LLM options
- **Hybrid AI Models**: Support for both local (Ollama) and cloud-based (Gemini API) language models
- **Document References**: View source documents that inform AI answers with relevance scores
- **PDF Integration**: Direct access to thesis PDFs via hash code identification system
- **Advanced Filtering & Sorting**: Filter by year, department, supervisor, and sort results
- **Statistics Dashboard**: Comprehensive analytics with visualizations, word clouds, and trend analysis
- **Supervisor Search**: Specialized search functionality for thesis supervisors
- **Expandable Results**: Toggle between short and full abstracts

---

## **Technology Stack**

### **Backend Technologies**
- **Framework**: Flask (Python) with RESTful API design
- **Search Engine**: Elasticsearch 8.x with vector search capabilities
- **AI Integration**: 
  - Ollama (local LLM hosting) supporting Llama 3.1/3.2 models
  - Google Gemini API (cloud-based) for enhanced performance
- **Vector Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Testing**: pytest for unit and integration testing
- **Data Processing**: Custom PDF processing and hash code generation

### **Frontend Technologies**
- **Framework**: React with modern hooks and functional components
- **Routing**: React Router for SPA navigation
- **HTTP Client**: Axios for API communication
- **Visualizations**: 
  - Recharts for statistical charts and graphs
  - React TagCloud for keyword visualization
- **Styling**: Custom CSS with responsive design

### **Infrastructure**
- **PDF Storage**: Docker-based storage service with PostgreSQL
- **Data Storage**: Elasticsearch indices for both traditional and semantic search
- **Development**: Git version control with modular architecture

---

## **System Architecture**

ThesisFinder follows a microservices-inspired architecture with five main components:

1. **Frontend (React)**: User interface and interaction layer
2. **Backend (Flask)**: API server and business logic
3. **Elasticsearch**: Search engine and data storage
4. **PDF Storage Service**: Document storage and retrieval
5. **AI Services**: Ollama (local) and Gemini API (cloud) for question answering

The system uses RESTful APIs for communication between components, enabling independent development and scaling of each service.

---

## **Installation Instructions**

### **Prerequisites**

Ensure the following are installed on your machine:

1. **Python 3.8+**
2. **Node.js 16+** and **npm**
3. **Elasticsearch 8.x**
4. **Ollama** (for local AI models)
5. **Docker & Docker Compose** (for PDF storage service)
6. **Git** (for version control)

### **Backend Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/FazakasNimrod/RAG-System-for-Theses.git
   cd RAG-System-for-Theses
   ```

2. **Create Python Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install google-generativeai  # For Gemini API support
   ```

4. **Configure Environment Variables**:
   ```bash
   # Create .env file in backend directory
   ELASTIC_USERNAME=your_username
   ELASTIC_PASSWORD=your_password
   OLLAMA_API_BASE=http://localhost:11434/api
   GEMINI_API_KEY=your_gemini_api_key  # Optional, for Gemini API
   ```

5. **Set Up Elasticsearch**:
   - Download from [official website](https://www.elastic.co/downloads/elasticsearch)
   - Extract to `/backend/elasticsearch` directory
   - Start Elasticsearch:
     ```bash
     cd backend/elasticsearch
     bin/elasticsearch    # Linux/Mac
     bin\elasticsearch.bat # Windows
     ```
   - Verify at `http://localhost:9200`

6. **Set Up PDF Storage Service**:
   ```bash
   cd ~/projects/pdf-storage
   docker-compose up -d
   ```
   - Verify at `http://localhost:5000/pdfs`

7. **Process and Index Documents**:
   ```bash
   # Extract metadata from PDFs
   python backend/scripts/pdf_processing/extract_text_v2.py
   python backend/scripts/pdf_processing/process_infos_theses.py

   # Create Elasticsearch indices
   python backend/scripts/data_loading/index_cs_theses.py
   python backend/scripts/data_loading/generate_infos_embeddings.py

   # Update hash codes for PDF integration
   python backend/scripts/data_loading/update_indices_with_hash_codes.py
   ```

8. **Set Up AI Models**:
   
   **For Ollama (Local):**
   ```bash
   # Install Ollama from ollama.ai
   ollama pull llama3.1:8b
   ollama pull llama3.2:3b
   ollama pull llama3.2:1b
   ```

   **For Gemini API (Cloud):**
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add to environment variables: `GEMINI_API_KEY=your_key_here`

9. **Run Backend**:
   ```bash
   cd backend
   flask run
   ```
   API available at `http://127.0.0.1:5000`

### **Frontend Setup**

1. **Navigate to Frontend**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run Frontend**:
   ```bash
   npm start
   ```
   Application available at `http://localhost:3000`

---

## **Usage Guide**

### **1. Traditional Search**
- **Basic Search**: Enter keywords for full-text search across abstracts
- **Phrase Search**: Enable exact phrase matching with quotes
- **Filters**: Apply year, department, and supervisor filters
- **Supervisor Search**: Dedicated search within supervisor names
- **Sorting**: Sort by relevance or year (ascending/descending)
- **Results**: View highlighted matches with expandable abstracts

### **2. Semantic Search**
- **Conceptual Queries**: Search by meaning, not just keywords
- **Similarity Scores**: View relevance scores for each result
- **Flexible Results**: Adjust number of results (1-50)
- **Cross-Language Understanding**: Find related concepts even with different terminology

### **3. AI Question Answering (RAG)**
- **Natural Language Queries**: Ask questions in plain English
- **Model Selection**: Choose between:
  - **Ollama Models** (Local):
    - Llama 3.1 8B: Best for complex reasoning
    - Llama 3.2 3B: Balanced performance
    - Llama 3.2 1B: Fastest responses
  - **Gemini Models** (Cloud):
    - Gemini 1.5 Pro: Most capable model
    - Gemini 1.5 Flash: Fast and efficient
- **Source References**: View documents used to generate answers
- **Context-Aware Responses**: Answers based on actual thesis content

### **4. Statistics Dashboard**
- **Overview Cards**: Total documents, supervisors, years, average abstract length
- **Filtering Options**: Department, year, supervisor-specific views
- **Visualizations**:
  - Research topics distribution (pie chart)
  - Yearly trends (bar chart)
  - Supervisor rankings
  - Research keywords word cloud
- **Recent Theses**: Latest submissions with metadata

### **5. PDF Document Access**
- **Direct Access**: Click "Go to PDF" from any search result
- **Hash-Based Routing**: Secure document identification
- **Browser Integration**: View PDFs directly in browser
- **Download Option**: Save documents locally

---

## **API Documentation**

### **Core Endpoints**

```
GET  /search                     # Traditional keyword search
GET  /search/semantic           # Semantic vector search
POST /search/rag               # AI question answering
GET  /search/models            # Available AI models
GET  /search/statistics        # Statistical data
GET  /search/statistics/supervisors  # Supervisor list
GET  /search/statistics/years  # Available years
GET  /search/document/<hash>   # Document by hash code
GET  /search/pdf/<hash>        # PDF redirect
```

### **Query Parameters**

**Search Endpoints:**
- `q`: Query string
- `year`: Filter by year
- `department`: Filter by department (cs/informatics)
- `sort`: Sort order (relevance/asc/desc)
- `phrase`: Enable phrase search (true/false)
- `search_supervisors`: Search in supervisor names (true/false)
- `limit`: Number of results (default: 50, max: 100)

**RAG Endpoint (POST):**
```json
{
  "query": "Your question here",
  "model": "llama3.1:8b",
  "top_k": 5,
  "department": "cs"
}
```

---

## **Project Structure**

```
ThesisFinder/
├── backend/
│   ├── app/
│   │   ├── app.py                    # Flask application entry
│   │   ├── routes.py                 # API endpoints
│   │   ├── search_services.py        # Search services
│   │   ├── ollama_rag_service.py     # RAG implementation
│   │   └── statistics_service.py     # Statistics calculations
│   ├── scripts/
│   │   ├── pdf_processing/           # PDF metadata extraction
│   │   ├── data_loading/            # Elasticsearch indexing
│   │   └── category_extraction/     # Topic categorization
│   ├── tests/
│   │   ├── unit_tests/              # Unit tests
│   │   └── integration_tests/       # Integration tests
│   └── elasticsearch/               # Elasticsearch installation
├── frontend/
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── pages/                   # Page components
│   │   ├── services/                # API communication
│   │   └── styles/                  # CSS styling
│   └── public/                      # Static assets
└── docs/                           # Documentation
```

---

## **Data Model**

### **Elasticsearch Indices**

**Base Document Structure:**
```json
{
  "author": "String",
  "supervisor": ["String"] | "String",
  "year": Number,
  "abstract": "String",
  "keywords": ["String"],
  "department": "cs" | "informatics",
  "hash_code": Number
}
```

**Semantic Index (Additional Field):**
```json
{
  "abstract_vector": [Float] // 384-dimensional embedding
}
```

### **Hash Code System**
- **Generation**: SHA-256 hash of normalized filename → 10-digit integer
- **Purpose**: Unique document identification across system components
- **Usage**: Links Elasticsearch documents to PDF storage

---

## **Performance Metrics**

Based on evaluation with 122 test queries:

| Metric | Lexical Search | Semantic Search |
|--------|---------------|-----------------|
| MRR | 0.893 | 0.906 |
| Recall@1 | 0.852 | 0.843 |
| Recall@3 | 0.921 | 0.965 |
| Recall@5 | 0.947 | 0.982 |

**Key Insights:**
- Semantic search excels at finding relevant documents in top 3-5 results
- Both methods achieve high accuracy (>85% first-result accuracy)
- Hybrid approach recommended for optimal user experience

---

## **Testing**

### **Running Tests**

```bash
# Unit tests
pytest tests/unit_tests/ -v

# Integration tests  
python run_integration_tests.py

# Specific test
pytest tests/unit_tests/test_statistics_service.py::TestClass::test_method -v
```

### **Test Coverage**
- **Unit Tests**: 23 tests covering core functionality
- **Integration Tests**: 9 tests covering API endpoints
- **Performance Tests**: Search accuracy evaluation
- **Components Tested**: Statistics service, search functionality, data processing

---

## **Troubleshooting**

### **Common Issues**

**Search Problems:**
- **No results**: Check Elasticsearch status and index existence
- **Slow performance**: Verify Elasticsearch memory allocation
- **Incorrect results**: Re-run indexing scripts

**PDF Integration:**
- **PDFs not loading**: Ensure Docker service is running (`docker-compose up -d`)
- **Wrong PDFs**: Run `update_indices_with_hash_codes.py`
- **Missing hash codes**: Check cleaned data files

**AI/RAG Issues:**
- **Ollama not working**: Verify service is running (`ollama list`)
- **Gemini API errors**: Check API key configuration
- **Slow responses**: Use smaller models (llama3.2:1b)
- **Out of memory**: Reduce model size or batch size

**Development Issues:**
- **Port conflicts**: Change ports in configuration
- **Environment variables**: Verify .env file setup
- **Dependencies**: Update requirements.txt packages

---

## **Performance Optimization**

### **Search Performance**
- **Elasticsearch**: Allocated 4GB+ RAM for optimal performance
- **Indexing**: Use bulk operations for large datasets
- **Queries**: Implement query caching for frequent searches

### **AI Performance**
- **Local Models**: Use GPU acceleration if available
- **Cloud Models**: Implement request batching for Gemini API
- **Caching**: Cache embeddings and frequent responses

---

## **Security Considerations**

- **API Keys**: Store in environment variables, never in code
- **PDF Access**: Hash-based identification prevents direct file access
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Implement for API endpoints (recommended)

---

## **Future Enhancements**

### **Short-term**
- User authentication and personalization
- Advanced filtering options (topic categories)
- Export functionality (citations, bibliographies)
- Mobile app development

### **Long-term**
- Multi-language support
- Collaborative features (notes, annotations)
- Advanced analytics dashboard
- Integration with academic databases
- Custom model fine-tuning for domain-specific tasks

---

## **Citation**

If you use ThesisFinder in your research, please cite:

```
Fazakas, N. (2025). ThesisFinder: Intelligent Search in Academic Theses. 
University "Sapientia" of Cluj-Napoca, Faculty of Technical and Human Sciences, Târgu Mureș.
```

---

## **Support**

- **Repository**: [GitHub](https://github.com/FazakasNimrod/RAG-System-for-Theses)
- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Comprehensive thesis documentation available in repository

---

**Enjoy exploring academic research with multiple search paradigms!** 📚🔍🤖