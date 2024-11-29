### **README: Theses Search Application**

---

## **Project Overview**
The Theses Search Application is a full-stack project designed to enable efficient searching, filtering, and sorting of academic theses stored in an Elasticsearch database. The application combines advanced search capabilities, including text-based and vector-based searches, with a modern React-based frontend for an intuitive user experience.

### **Key Features**
- **Full-Text Search**: Search theses by abstract, keywords, and author.
- **Filters**: Filter results by publication year.
- **Sorting**: Sort results in ascending or descending order.
- **Highlighting**: Highlights search keywords in the results.
- **Vector Search**: Enables semantic similarity searches for advanced use cases.
- **Modern UI**: A responsive, aesthetically pleasing frontend with intuitive design.

---

## **Technology Stack**
- **Backend**: Flask (Python)
- **Search Engine**: Elasticsearch (with vector search capabilities)
- **Frontend**: React
- **Styling**: CSS
- **Deployment**: Localhost for development

---

## **Installation Instructions**

### **Prerequisites**
Ensure the following are installed on your machine:
1. **Python 3.8+**
2. **Node.js 16+**
3. **npm** (comes with Node.js)
4. **Elasticsearch** (minimum version 8.x)
5. **pip** (Python package installer)

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
   - Install Elasticsearch locally.
   - Start the Elasticsearch service:
     ```bash
     ./bin/elasticsearch
     ```
   - Add the Elasticsearch directory to `.gitignore`.

5. **Load Data into Elasticsearch**:
   - Ensure your `theses` data is available as a JSON file.
   - Use the Python script (index_theses.py) to load data into the `theses` index.

6. **Run the Backend**:
   ```bash
   flask run
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

### **Frontend Setup**
1. **Navigate to the `frontend` Directory**:
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

## **Usage Instructions**
1. Open the browser and navigate to `http://localhost:3000`.
2. Enter your search term in the search bar.
3. Optionally filter by year and choose a sorting order.
4. Click **Search** to display the results.
5. View highlighted keywords in the results list.

---

## **Folder Structure**

### **Backend**
- **`backend/app/app.py`**: Flask application entry point.
- **`backend/app/routes.py`**: Contains search-related API endpoints.
- **`backend/app/services.py`**: Handles interaction with Elasticsearch.
- **`requirements.txt`**: Python dependencies.
- **`queries/`**: Contains queries for the Elasticsearch.
- **`scripts/index_theses.py`** Load the documents to the index.

### **Frontend**
- **`src/components`**:
  - `SearchBar.js`: Contains the search bar component.
  - `ResultsList.js`: Displays the search results.
- **`src/pages`**:
  - `SearchPage.js`: Main page combining components.
- **`src/services`**:
  - `elasticsearchService.js`: Handles API calls to the backend.
- **CSS Files**: Styling for components.

---

## **Troubleshooting**
- **CORS Error**: Add CORS headers in the Flask backend using `flask-cors`.
- **Elasticsearch Connection Issues**: Ensure Elasticsearch is running locally and configured for the correct port.
- **No Results Returned**: Check the search query in Elasticsearch and verify data availability in the `theses` index.

---

## **Future Enhancements**
- **Authentication**: Add user login and personalized search histories.
- **Pagination**: Handle large result sets with paginated responses.
- **Cloud Deployment**: Deploy the application using AWS or Heroku for broader access.
- **Improved Styling**: Enhance responsiveness and accessibility.

---

Enjoy using the Theses Search Application! 😊