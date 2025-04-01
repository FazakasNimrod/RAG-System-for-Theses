import os
import re
import hashlib
import psycopg2
from flask import Flask, jsonify, send_from_directory, abort
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'pdf_storage'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn

def title_to_hash_code(title):
    """
    Convert a title to a unique 10-digit hash code
    
    Args:
        title (str): The title of the PDF
    
    Returns:
        int: A unique 10-digit hash code representation of the title
    """
    # Normalize the title
    def normalize_title(title):
        # Convert to lowercase
        normalized = title.lower()
        
        # Remove special characters and extra whitespace
        normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    # Normalize the title
    normalized_title = normalize_title(title)
    
    # Create a hash of the normalized title
    hash_object = hashlib.sha256(normalized_title.encode())
    
    # Convert the hash to a large integer
    full_hash = int(hash_object.hexdigest(), 16)
    
    # Ensure 10-digit number
    # Use modulo to limit to 10 digits while maintaining uniqueness
    ten_digit_hash = full_hash % 10000000000
    
    return ten_digit_hash

def create_tables():
    """Create tables if they don't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create PDFs table with hash_code
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pdfs (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                category VARCHAR(50) NOT NULL,
                file_path VARCHAR(512) NOT NULL,
                hash_code BIGINT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(filename, category),
                UNIQUE(hash_code)
            );
            
            CREATE INDEX IF NOT EXISTS idx_pdfs_category ON pdfs(category);
            CREATE INDEX IF NOT EXISTS idx_pdfs_hash_code ON pdfs(hash_code);
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

def upload_pdfs_from_folders():
    """Upload PDF file paths from specified folders to the database"""
    pdf_base_path = '/pdfs'
    categories = ['informatics', 'cscience']
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Track uploaded PDFs
        uploaded_count = 0
        
        # Iterate through categories
        for category in categories:
            category_path = os.path.join(pdf_base_path, category)
            
            # Ensure the category path exists
            if not os.path.exists(category_path):
                print(f"Category path not found: {category_path}")
                continue
            
            # List PDF files in the category folder
            for filename in os.listdir(category_path):
                if filename.lower().endswith('.pdf'):
                    # Create full file path
                    file_path = os.path.join(category, filename)
                    
                    try:
                        # Generate hash code from filename (you might want to extract title from PDF metadata later)
                        hash_code = title_to_hash_code(filename)
                        
                        # Insert PDF file path into database, ignoring duplicates
                        cur.execute("""
                            INSERT INTO pdfs (filename, category, file_path, hash_code) 
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (filename, category) DO NOTHING
                        """, (filename, category, file_path, hash_code))
                        
                        # Check if a row was inserted
                        if cur.rowcount > 0:
                            uploaded_count += 1
                            print(f"Uploaded: {filename} (Category: {category}, Hash Code: {hash_code})")
                    
                    except Exception as file_err:
                        print(f"Error processing file {filename}: {file_err}")
        
        # Commit the transaction
        conn.commit()
        print(f"Total PDFs uploaded: {uploaded_count}")
        
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"Error uploading PDFs: {e}")

# Create tables and upload PDFs when the application starts
create_tables()
upload_pdfs_from_folders()

@app.route('/')
def hello():
    """Simple health check endpoint"""
    return "PDF Storage Service is Active!", 200

@app.route('/pdfs')
def list_pdfs():
    """List PDFs in the database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch PDF metadata
        cur.execute("SELECT id, filename, category, file_path, hash_code, uploaded_at FROM pdfs")
        pdfs = cur.fetchall()
        
        # Convert to list of dictionaries
        pdf_list = [
            {
                'id': pdf[0], 
                'filename': pdf[1], 
                'category': pdf[2],
                'file_path': pdf[3],
                'hash_code': pdf[4],
                'uploaded_at': str(pdf[5])
            } for pdf in pdfs
        ]
        
        cur.close()
        conn.close()
        
        return jsonify(pdf_list), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<int:hash_code>')
def open_pdf(hash_code):
    """Open a specific PDF by hash code"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch PDF file path using hash code
        cur.execute("SELECT file_path FROM pdfs WHERE hash_code = %s", (hash_code,))
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not result:
            abort(404, description="PDF not found")
        
        # Send PDF file from the /pdfs directory
        return send_from_directory('/pdfs', result[0], mimetype='application/pdf')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pdfs/<category>')
def list_pdfs_by_category(category):
    """List PDFs in a specific category"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch PDF metadata for specific category
        cur.execute("SELECT id, filename, category, file_path, hash_code, uploaded_at FROM pdfs WHERE category = %s", (category,))
        pdfs = cur.fetchall()
        
        # Convert to list of dictionaries
        pdf_list = [
            {
                'id': pdf[0], 
                'filename': pdf[1], 
                'category': pdf[2],
                'file_path': pdf[3],
                'hash_code': pdf[4],
                'uploaded_at': str(pdf[5])
            } for pdf in pdfs
        ]
        
        cur.close()
        conn.close()
        
        return jsonify(pdf_list), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Comprehensive health check"""
    try:
        # Check database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM pdfs")
        pdf_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "pdf_count": pdf_count,
            "message": "PDF Storage Service is running smoothly"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'false').lower() == 'true')
