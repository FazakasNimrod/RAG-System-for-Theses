from sentence_transformers import SentenceTransformer
import requests
import json
from typing import List, Dict, Any, Optional
import os
import google.generativeai as genai

modell_name = 'all-MiniLM-L6-v2'
#modell_name = 'bge-small-en' 
#modell_name = 'bge-base-en'
#modell_name = 'bge-large-en'

OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/api")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

AVAILABLE_MODELS = [
    {
        "id": "llama3.1:8b",
        "name": "Llama 3.1 (8B)",
        "description": "Meta's 8 billion parameter model, good for general knowledge questions",
        "provider": "ollama"
    },
    {
        "id": "llama3.2:1b",
        "name": "Llama 3.2 (1B)",
        "description": "Smallest and fastest model, good for simple questions",
        "provider": "ollama"
    },
    {
        "id": "llama3.2:3b",
        "name": "Llama 3.2 (3B)",
        "description": "Balanced model for performance and quality",
        "provider": "ollama"
    },
    {
        "id": "gemini-1.5-flash",
        "name": "Gemini 1.5 Flash",
        "description": "Google's fast and efficient model, excellent for quick responses",
        "provider": "gemini"
    },
    {
        "id": "gemini-1.5-pro",
        "name": "Gemini 1.5 Pro",
        "description": "Google's most capable model, best for complex reasoning",
        "provider": "gemini"
    }
]

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(modell_name)
    return _embedding_model

def retrieve_documents(es, query: str, top_k: int = 5, department: str = None) -> List[Dict[str, Any]]:
    """
    Retrieve documents based on semantic similarity for RAG

    :param es: Elasticsearch client instance
    :param query: Query string
    :param top_k: Number of documents to retrieve
    :param department: Optional filter by department ('cs' or 'informatics')
    :return: List of retrieved documents
    """
    model = get_embedding_model()
    
    query_vector = model.encode(query).tolist()
    
    filter_clause = []
    if department:
        filter_clause.append({"term": {"department": department}})
    
    search_query = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "filter": filter_clause
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'abstract_vector') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        },
        "size": top_k
    }
    
    if department == "cs":
        indices = ["cs_theses_semantic"]
    elif department == "informatics":
        indices = ["infos_theses_semantic"]
    else:
        indices = ["cs_theses_semantic", "infos_theses_semantic"] 
    
    response = es.search(index=",".join(indices), body=search_query)
    
    return response['hits']['hits']

def prepare_context(documents: List[Dict[str, Any]]) -> str:
    """
    Prepare context from retrieved documents
    
    :param documents: List of retrieved documents
    :return: Context string for RAG
    """
    context = "RELEVANT DOCUMENTS:\n\n"
    
    for i, doc in enumerate(documents, 1):
        source = doc["_source"]
        author = source.get("author", "Unknown Author")
        year = source.get("year", "Unknown Year")
        abstract = source.get("abstract", "No abstract available")
        department = source.get("department", "Unknown Department")
        
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."
        
        context += f"[{author} ({year})]\n"
        context += f"Department: {department}\n"
        context += f"Abstract: {abstract}\n\n"
    
    return context

def generate_answer_with_ollama(model_id: str, context: str, query: str) -> str:
    """Generate answer using Ollama API"""
    prompt = f"""You are a knowledgeable research expert who specializes in academic papers and theses.

I've provided some relevant research documents below. Using ONLY this information, answer the following question directly and concisely.

Important guidelines:
- Answer in a natural, conversational way - as if explaining to a colleague
- When referring to the theses, use the author names (e.g., "As demonstrated by Smith (2023)..." or "The research by Jones (2022) shows...")
- Do not use phrases like "Document 1" or "Document 2" - always refer to the authors by name
- Keep your answer focused and concise
- If the documents don't contain relevant information, simply state that you don't have enough information
- Don't enumerate your points unless absolutely necessary

{context}

Question: {query}

Answer:"""

    try:
        response = requests.post(
            f"{OLLAMA_API_BASE}/generate",
            json={
                "model": model_id,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 350 
                }
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        print(f"Error calling Ollama API: {str(e)}")
        return f"I encountered an error while generating a response: {str(e)}"

def generate_answer_with_gemini(model_id: str, context: str, query: str) -> str:
    """Generate answer using Gemini API"""
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
    
    prompt = f"""You are a knowledgeable research expert who specializes in academic papers and theses.

I've provided some relevant research documents below. Using ONLY this information, answer the following question directly and concisely.

Important guidelines:
- Answer in a natural, conversational way - as if explaining to a colleague
- When referring to the theses, use the author names (e.g., "As demonstrated by Smith (2023)..." or "The research by Jones (2022) shows...")
- Do not use phrases like "Document 1" or "Document 2" - always refer to the authors by name
- Keep your answer focused and concise
- If the documents don't contain relevant information, simply state that you don't have enough information
- Don't enumerate your points unless absolutely necessary

{context}

Question: {query}

Answer:"""

    try:
        model = genai.GenerativeModel(model_id)
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=350,
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return f"I encountered an error while generating a response: {str(e)}"

def generate_rag_response(es, query: str, model_id: str, top_k: int = 5, department: str = None) -> Dict[str, Any]:
    """
    Generate RAG response
    
    :param es: Elasticsearch client instance
    :param query: Query string
    :param model_id: Ollama model ID or Gemini model ID
    :param top_k: Number of documents to retrieve
    :param department: Optional filter by department ('cs' or 'informatics')
    :return: RAG response with answer and references
    """
    try:
        model_info = next((m for m in AVAILABLE_MODELS if m["id"] == model_id), None)
        if not model_info:
            return {
                "error": f"Model {model_id} not found",
                "answer": "The requested model is not available."
            }
        
        model_name = model_info["name"]
        provider = model_info["provider"]
        
        documents = retrieve_documents(es, query, top_k, department)
        
        context = prepare_context(documents)
        
        if provider == "ollama":
            answer = generate_answer_with_ollama(model_id, context, query)
        elif provider == "gemini":
            answer = generate_answer_with_gemini(model_id, context, query)
        else:
            answer = f"Unknown provider: {provider}"
        
        references = []
        for doc in documents:
            source = doc["_source"]
            references.append({
                "id": doc["_id"],
                "author": source.get("author", "Unknown"),
                "year": source.get("year", "Unknown"),
                "score": doc["_score"],
                "abstract_snippet": source.get("abstract", "")[:150] + "...",
                "department": source.get("department", "Unknown"),
                "hash_code": source.get("hash_code", None)
            })
        
        return {
            "answer": answer,
            "references": references,
            "model": model_name,
            "provider": provider
        }
        
    except Exception as e:
        print(f"Error in RAG process: {str(e)}")
        return {
            "error": str(e),
            "answer": "I encountered an error while trying to answer your question.",
            "references": []
        }

def get_available_models() -> List[Dict[str, str]]:
    """Get list of available models from both Ollama and Gemini"""
    available_models = []
    
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/tags", timeout=5)
        if response.status_code == 200:
            ollama_models = response.json().get("models", [])
            available_model_names = {model["name"] for model in ollama_models}
            
            for model in AVAILABLE_MODELS:
                if model["provider"] == "ollama" and model["id"] in available_model_names:
                    available_models.append(model)
    except Exception as e:
        print(f"Error checking Ollama models: {str(e)}")
    
    if GEMINI_API_KEY:
        for model in AVAILABLE_MODELS:
            if model["provider"] == "gemini":
                available_models.append(model)
    else:
        print("Gemini API key not configured - Gemini models unavailable")
    
    if not available_models:
        return AVAILABLE_MODELS
    
    return available_models
