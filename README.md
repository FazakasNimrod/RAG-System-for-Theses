# **Theses Search & Question-Answering Application**

## **Project Overview**

This application is a comprehensive full-stack solution for searching, analyzing, and interacting with academic theses. Built with a powerful combination of traditional search, semantic search, and AI-powered question answering capabilities, it enables researchers to find information more effectively through multiple search paradigms.

### **Key Features**

- **Traditional Search**: Full-text search with keyword highlighting
- **Phrase Search**: Exact phrase matching for precise queries
- **Semantic Search**: Vector-based semantic similarity search
- **AI-Powered Question Answering**: Ask natural language questions about research topics
- **Document References**: View source documents that inform AI answers
- **PDF Integration**: Direct access to thesis PDFs via hash code integration
- **Filtering & Sorting**: Filter by year, department and sort results
- **Expandable Results**: Toggle between short and full abstracts
- **Authentication**: User registration and login system (coming soon...)

---

## **Technology Stack**

- **Backend**: Flask (Python)
- **Search Engine**: Elasticsearch with vector search capabilities
- **Frontend**: React
- **AI Models**: Ollama with Llama models (local LLM integration)
- **Vector Embeddings**: SentenceTransformers
- **PDF Storage**: Docker-based PDF storage service with hash code identification
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
6. **Docker & Docker Compose** (for PDF storage service)

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

   - Download Elasticsearch from the [official website](https://www.elastic.co/downloads/elasticsearch)
   - Extract the downloaded archive into the `/backend/elasticsearch` directory of your project
   - Start the Elasticsearch service:

     ```bash
     # Navigate to the elasticsearch directory
     cd backend/elasticsearch

     # Start Elasticsearch
     bin/elasticsearch    # Linux/Mac
     bin\elasticsearch.bat # Windows
     ```

   - Verify Elasticsearch is running by visiting `http://localhost:9200` in your browser

5. **Set Up PDF Storage Service**:

   - Ensure Docker and Docker Compose are installed
   - Navigate to the PDF storage project directory:
     ```bash
     cd ~/projects/pdf-storage
     ```
   - Start the PDF storage service:
     ```bash
     docker-compose up -d
     ```
   - Verify it's running: `http://localhost:5000/pdfs`

6. **Process PDF Documents and Update Indices**:

   ```bash
   # Process CS department theses
   python backend/scripts/pdf_processing/extarct_text_v2.py

   # Process Informatics department theses
   python backend/scripts/pdf_processing/process_infos_theses.py

   # Create and update the Elasticsearch indices
   python backend/scripts/data_loading/index_cs_theses.py
   python backend/scripts/data_loading/generate_infos_embeddings.py

   # Update all indices with hash codes from cleaned data
   python backend/scripts/data_loading/update_indices_with_hash_codes.py
   ```

7. **Set Up Ollama** (for RAG functionality):

   - Install Ollama from [ollama.ai/download](https://ollama.ai/download)
   - Pull the required models:
     ```bash
     ollama pull llama3.1:8b
     ollama pull llama3.2:1b
     ollama pull llama3.2:3b
     ```

8. **Run the Backend**:
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
- Filter by year and department and sort as needed
- View highlighted matches in results
- Click "Go to PDF" to view the original thesis document

### **2. Semantic Search**

- Navigate to the "Semantic Search" page
- Enter conceptual queries (doesn't require exact keyword matches)
- Adjust the number of results to display
- View results ranked by semantic similarity
- Access original PDF documents with one click

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
  - `/search/document/<hash_code>`: Get document by hash code
  - `/search/pdf/<hash_code>`: Redirect to PDF storage

- **Data Processing**:
  - `scripts/pdf_processing/`: Extract metadata from PDFs
  - `scripts/data_loading/`: Index documents in Elasticsearch
  - `scripts/data_loading/update_indices_with_hash_codes.py`: Update hash codes

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

- **Services**:
  - elasticsearchService.js: Handle search requests
  - ragService.js: RAG functionality and PDF access

---

## **PDF Integration System**

The application integrates with a Docker-based PDF storage service that uses hash codes to identify documents:

1. **Hash Code Generation**:

   - Each PDF is assigned a unique 10-digit hash code
   - Hash codes are generated from filenames using SHA-256 hashing

2. **Data Flow**:

   - PDF processing scripts extract metadata and generate hash codes
   - Hash codes are stored in cleaned JSON data files
   - Elasticsearch indices are updated with hash codes
   - Frontend uses hash codes to link to the PDF storage service

3. **Viewing PDFs**:
   - When a user clicks "Go to PDF" or "View Document"
   - The application uses the document's hash code to locate the file
   - User is sent to the PDF storage service URL with the hash code
   - PDF storage service serves the document based on hash code

---

## **Troubleshooting**

### **Common PDF Integration Issues**

- **PDFs not loading**: Ensure PDF storage service is running (`docker-compose up -d`)
- **Wrong PDFs loading**: Run `update_indices_with_hash_codes.py` to fix hash codes
- **Missing hash codes**: Check the cleaned data files and update the indices

### **Elasticsearch Issues**

- **Connection errors**: Ensure Elasticsearch is running
- **Missing indices**: Run the indexing scripts
- **Search returns no results**: Check your search query and filters

### **Ollama Issues**

- **RAG not working**: Ensure Ollama is running and models are pulled
- **Slow responses**: Try using smaller models like llama3.2:1b
- **Out of memory errors**: Reduce model size or response length

---

## **Future Enhancements**

- Backend implementation for authentication system
- Conversational memory for follow-up questions
- User-specific search history and preferences
- Additional filtering options
- Custom model fine-tuning for specific domains
- Enhanced PDF viewer integration

---

Enjoy exploring academic research with multiple search paradigms! 📚🔍
