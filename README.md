# **Theses Search & Question-Answering Application**

## **Project Overview**

This application is a comprehensive full-stack solution for searching, analyzing, and interacting with academic theses. Built with a powerful combination of traditional search, semantic search, and AI-powered question answering capabilities, it enables researchers to find information more effectively through multiple search paradigms.

### **Key Features**

- **Traditional Search**: Full-text search with keyword highlighting
- **Phrase Search**: Exact phrase matching for precise queries
- **Semantic Search**: Vector-based semantic similarity search
- **AI-Powered Question Answering**: Ask natural language questions about research topics
- **Document References**: View source documents that inform AI answers
- **Filtering & Sorting**: Filter by year and sort results
- **Expandable Results**: Toggle between short and full abstracts
- **Authentication**: User registration and login system (coming soon...)

---

## **Technology Stack**

- **Backend**: Flask (Python)
- **Search Engine**: Elasticsearch with vector search capabilities
- **Frontend**: React
- **AI Models**: Ollama with Llama models (local LLM integration)
- **Vector Embeddings**: SentenceTransformers
- **Styling**: Custom CSS

---

## **Installation Instructions**

### **Prerequisites**

Ensure the following are installed on your machine:

1. **Python 3.8+**
2. **Node.js 16+**
3. **npm** (comes with Node.js)
4. **Elasticsearch** (minimum version 8.x)
5. **Ollama** (for AI question answering)

### **Backend Setup**

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Python Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. **Install Backend Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Elasticsearch**:

   - Start the Elasticsearch service
   - Load data into the basic and semantic indices

5. **Set Up Ollama** (for RAG functionality):

   - Install Ollama from [ollama.ai/download](https://ollama.ai/download)
   - Pull the required models:
     ```bash
     ollama pull llama3.1:8b
     ollama pull llama3.2:1b
     ollama pull llama3.2:3b
     ```

6. **Run the Backend**:
   ```bash
   flask run
   ```
   The API will be available at `http://127.0.0.1:5000`.

### **Frontend Setup**

1. **Navigate to the Frontend Directory**:

   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**:

   ```bash
   npm install
   ```

3. **Run the Frontend**:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

---

## **Usage Guide**

### **1. Traditional Search**

- Enter keywords in the search bar
- Optionally enable phrase search for exact matching
- Filter by year and sort as needed
- View highlighted matches in results

### **2. Semantic Search**

- Navigate to the "Semantic Search" page
- Enter conceptual queries (doesn't require exact keyword matches)
- Adjust the number of results to display
- View results ranked by semantic similarity

### **3. AI Question Answering**

- Navigate to the "Ask Questions" page
- Select a model (options vary by size and performance)
- Type your research question
- View generated answer and source documents
- Click "View Document" to access original PDFs

### **4. User Authentication**

- Sign up for a new account to save preferences
- Sign in to access personalized features

---

## **Project Structure**

### **Backend**

- **API Endpoints**:
  - `/search`: Traditional and phrase search
  - `/search/semantic`: Vector-based semantic search
  - `/search/rag`: Retrieval-augmented generation for question answering
  - `/search/models`: Available AI models

### **Frontend**

- **Pages**:
  - Search (Home)
  - Semantic Search
  - Ask Questions (RAG)
  - Sign Up/Sign In
- **Components**:
  - SearchBar
  - ResultsList
  - AbstractContent
  - Sidebar

---

## **Requirements**

### **Backend Dependencies**

- Flask
- Elasticsearch
- SentenceTransformers
- Requests
- Python-dotenv
- Flask-CORS

### **Frontend Dependencies**

- React
- React Router
- Axios
- CSS (custom styling)

---

## **Troubleshooting**

- **Elasticsearch Connection**: Ensure Elasticsearch is running and properly configured
- **Ollama Models**: Verify that Ollama is running and the required models are downloaded
- **Vector Search**: Make sure the semantic index is properly created with vector embeddings
- **CORS Issues**: Check that Flask-CORS is properly configured

---

## **Future Enhancements**

- Backend implementation for authentication system
- Conversational memory for follow-up questions
- User-specific search history and preferences
- Additional filtering options
- Custom model fine-tuning for specific domains
- PDF viewer integration

---

Enjoy exploring academic research with multiple search paradigms! 📚🔍
