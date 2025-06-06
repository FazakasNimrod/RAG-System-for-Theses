# Enhanced RAG System with Ollama

This implementation provides a comprehensive Retrieval-Augmented Generation (RAG) system that integrates seamlessly with your thesis search application using [Ollama](https://ollama.ai/) for local LLM processing.

## Overview

The enhanced RAG system combines:
1. **Advanced Document Retrieval**: Multi-index semantic search across CS and Informatics theses
2. **Intelligent Context Building**: Relevance-based document selection and summarization
3. **Local LLM Processing**: Ollama-powered answer generation with multiple model options
4. **Smart Filtering**: Department-based document filtering for targeted results
5. **Reference Tracking**: Complete source attribution with PDF access integration

## Prerequisites

### 1. Ollama Setup

- Download and install Ollama from [ollama.ai/download](https://ollama.ai/download)
- Pull the required models:
  ```bash
  ollama pull llama3.1:8b    # High-quality, slower responses
  ollama pull llama3.2:1b    # Fastest responses for simple questions
  ollama pull llama3.2:3b    # Balanced performance (default)
  ```

### 2. Backend Dependencies

Ensure you have all required Python packages:

```bash
pip install flask flask-cors elasticsearch python-dotenv sentence-transformers requests
```

### 3. Elasticsearch Indices

The RAG system requires properly configured semantic indices:
- `cs_theses_semantic`: Computer Science theses with vector embeddings
- `infos_theses_semantic`: Informatics theses with vector embeddings

## Enhanced Features

### 1. **Multi-Model Support**

The system supports three different Ollama models optimized for different use cases:

```javascript
// Available models with automatic selection based on question complexity
{
  "llama3.1:8b": "Best for complex research questions and detailed analysis",
  "llama3.2:1b": "Fastest responses for simple factual questions", 
  "llama3.2:3b": "Balanced performance for most questions (default)"
}
```

### 2. **Department-Specific Filtering**

Target your questions to specific academic departments:

```bash
# Search only Computer Science theses
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "neural network architectures", "department": "cs"}'

# Search only Informatics theses  
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "database optimization", "department": "informatics"}'
```

### 3. **Configurable Document Retrieval**

Adjust the number of reference documents for different question types:

```javascript
{
  "query": "What are the latest trends in IoT security?",
  "top_k": 8,        // Retrieve more documents for broader topics
  "model": "llama3.1:8b"
}
```

### 4. **Advanced Context Processing**

The system intelligently processes retrieved documents:
- **Relevance scoring**: Documents ranked by semantic similarity
- **Context optimization**: Abstracts trimmed for optimal LLM processing
- **Reference preservation**: Complete source information maintained

## File Structure

```
backend/app/
├── ollama_rag_service.py     # Enhanced RAG service with multi-model support
├── routes.py                 # API endpoints with department filtering
├── services.py               # Core search functionality
└── statistics_service.py     # Analytics integration

frontend/src/
├── pages/RagPage/
│   ├── RagPage.js           # Enhanced UI with model selection
│   └── RagPage.css          # Responsive styling
├── services/
│   └── ragService.js        # Frontend API integration
└── components/              # Reusable UI components
```

## API Usage Examples

### Basic Question Answering

```bash
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do IoT devices communicate with each other?",
    "model": "llama3.2:3b",
    "top_k": 5
  }'
```

### Research-Focused Questions

```bash
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main challenges in implementing machine learning for medical imaging?",
    "model": "llama3.1:8b",
    "top_k": 8,
    "department": "cs"
  }'
```

### Quick Factual Queries

```bash
curl -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What programming languages are used for web development?",
    "model": "llama3.2:1b",
    "top_k": 3
  }'
```

## Response Format

The enhanced RAG system returns comprehensive responses:

```json
{
  "answer": "Based on the research theses, IoT devices communicate through several protocols...",
  "references": [
    {
      "id": "cs_1",
      "author": "Bács Bernát",
      "year": 2023,
      "score": 0.87,
      "abstract_snippet": "The system uses MQTT communication protocols...",
      "department": "cs",
      "hash_code": 6375406094
    }
  ],
  "model": "Llama 3.2 (3B)"
}
```

## Frontend Integration

### Enhanced User Interface

The RAG page includes:
- **Model selection dropdown**: Choose appropriate LLM for your question
- **Department filtering**: Target specific academic areas  
- **Document count slider**: Adjust reference depth
- **Real-time status**: Connection status and processing indicators
- **Interactive references**: Direct PDF access via hash codes

### Smart Question Suggestions

The interface provides contextual help:
- Model recommendations based on question complexity
- Department suggestions for specialized topics
- Document count guidance for different question types

## Performance Optimization

### Model Selection Guidelines

- **llama3.2:1b**: Use for simple factual questions, definitions, basic explanations
- **llama3.2:3b**: Default choice for most research questions, good balance
- **llama3.1:8b**: Use for complex analysis, detailed comparisons, multi-part questions

### Document Retrieval Strategy

```javascript
// Recommended top_k values based on question type
{
  "simple_facts": 3,           // Basic definitions, single concepts
  "specific_research": 5,      // Focused research questions (default)
  "broad_topics": 8,          // Complex multi-faceted questions
  "comprehensive_analysis": 10 // Detailed comparative studies
}
```

### Performance Monitoring

```bash
# Check available models
curl "http://127.0.0.1:5000/search/models"

# Monitor response times for optimization
curl -w "@curl-format.txt" -X POST "http://127.0.0.1:5000/search/rag" \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'
```

## Integration with PDF Storage

The RAG system seamlessly integrates with the PDF storage service:

```javascript
// Each reference includes hash_code for direct PDF access
const openPDF = (reference) => {
  const pdfUrl = `http://localhost:5000/${reference.hash_code}`;
  window.open(pdfUrl, '_blank');
};
```

## Advanced Configuration

### Custom Prompt Engineering

Modify prompts in `ollama_rag_service.py`:

```python
# Customize the prompt template for specific domains
prompt = f"""You are a specialist in {department} research...
{context}
Question: {query}
Answer:"""
```

### Model Parameters

Fine-tune generation parameters:

```python
"options": {
    "temperature": 0.7,    # Control randomness (0.1-1.0)
    "top_p": 0.9,         # Control diversity (0.1-1.0)  
    "top_k": 40,          # Control selection pool (1-100)
    "num_predict": 350    # Maximum response length
}
```

### Department-Specific Optimization

```python
# Optimize retrieval for different departments
if department == "cs":
    # Boost algorithm and implementation keywords
    boost_terms = ["algorithm", "implementation", "performance"]
elif department == "informatics":
    # Boost system and application keywords  
    boost_terms = ["system", "application", "database"]
```

## Troubleshooting

### Common Issues and Solutions

1. **Models not appearing in UI**:
   ```bash
   # Verify Ollama is running
   ollama list
   
   # Pull missing models
   ollama pull llama3.2:3b
   ```

2. **Slow response times**:
   - Use smaller models (llama3.2:1b) for simple questions
   - Reduce `top_k` value for faster retrieval
   - Lower `num_predict` for shorter responses

3. **Empty or poor answers**:
   - Increase `top_k` for more context
   - Try different department filtering
   - Use more specific questions

4. **Connection errors**:
   ```bash
   # Check Ollama status
   curl http://localhost:11434/api/tags
   
   # Restart Ollama if needed
   ollama serve
   ```

### Performance Monitoring

```bash
# Monitor Ollama resource usage
ollama ps

# Check model loading status
ollama list
```

## Security Considerations

- **Local processing**: All LLM processing happens locally
- **No data transmission**: Research content never leaves your infrastructure  
- **Access control**: PDF access controlled via hash codes
- **Input validation**: Queries sanitized before processing

## Future Enhancements

### Planned Features

1. **Conversation memory**: Multi-turn question answering
2. **Source highlighting**: Exact quote attribution in references
3. **Question suggestions**: AI-powered follow-up questions
4. **Export functionality**: Save Q&A sessions as reports
5. **Advanced analytics**: Question pattern analysis
6. **Custom model fine-tuning**: Domain-specific model adaptation

### Integration Possibilities

- **Citation generation**: Automatic academic citations
- **Research assistance**: Literature review support
- **Thesis writing**: AI-powered writing assistance
- **Collaboration tools**: Shared research spaces
- **Version control**: Track research question evolution

---

## Quick Start Checklist

- [ ] Ollama installed and running
- [ ] Required models pulled (llama3.1:8b, llama3.2:1b, llama3.2:3b)
- [ ] Elasticsearch indices created with embeddings
- [ ] Backend dependencies installed
- [ ] PDF storage service running
- [ ] Frontend connected to backend API

For additional support, check the main project documentation or visit the [Ollama documentation](https://ollama.ai/docs).
