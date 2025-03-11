# RAG System with Ollama

This implementation integrates your thesis search application with [Ollama](https://ollama.ai/) to provide a powerful Retrieval-Augmented Generation (RAG) system.

## Overview

The system uses:
1. Your Elasticsearch index for document retrieval
2. Sentence Transformers for embedding queries
3. Ollama for running local LLMs to generate answers

## Prerequisites

### 1. Ollama Setup

- Download and install Ollama from [ollama.ai/download](https://ollama.ai/download)
- Pull the necessary models:
  ```bash
  ollama pull llama3.1:8b
  ollama pull llama3.2:1b
  ollama pull llama3.2:3b
  ```

### 2. Backend Setup

Make sure you have the required Python packages:

```bash
pip install flask flask-cors elasticsearch python-dotenv sentence-transformers requests
```

## How It Works

1. **Query Processing**:
   - User enters a question
   - The question is converted to a vector embedding

2. **Document Retrieval**:
   - The system searches the semantic index for relevant documents
   - Documents are ranked by semantic similarity

3. **Answer Generation**:
   - The system prepares a prompt with retrieved documents
   - The selected Ollama model generates an answer
   - References are returned with the answer

## File Structure

- `ollama_rag_service.py`: Main service for Ollama integration
- `updated_routes_ollama.py`: API endpoints
- `updated_ragService.js`: Frontend service to communicate with the API
- `updated_RagPage.js`: React component for the RAG UI
- `updated_RagPage.css`: Styling for the RAG page

## Customization

### Adding More Models

To add more models, update the `AVAILABLE_MODELS` list in `ollama_rag_service.py`:

```python
AVAILABLE_MODELS = [
    {
        "id": "your-model-name",
        "name": "Display Name",
        "description": "Description of the model"
    },
    # ...
]
```

Then pull the model in Ollama:

```bash
ollama pull your-model-name
```

### Adjusting Generation Parameters

You can adjust the generation parameters in the `generate_answer_with_ollama` function in `ollama_rag_service.py`:

```python
response = requests.post(
    f"{OLLAMA_API_BASE}/generate",
    json={
        "model": model_id,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,  # Adjust this to control randomness
            "top_p": 0.9,        # Adjust this to control diversity
            "top_k": 40,         # Adjust this to control selection pool
            "num_predict": 512   # Adjust maximum response length
        }
    },
    timeout=60
)
```

## Troubleshooting

- **Models not appearing**: Ensure Ollama is running and the models are pulled
- **Slow responses**: For faster responses, use the smaller models (llama3.2:1b)
- **Out of memory errors**: Try using a smaller model or reducing the `num_predict` value

## Advanced Features

- **Streaming responses**: Can be enabled by modifying the code to use Ollama's streaming API
- **Multimodal models**: Can be added if you pull models like `llava` or `bakllava`
