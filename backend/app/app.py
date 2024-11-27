from flask import Flask, g
from flask_cors import CORS
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from routes import search_routes

# Load environment variables
load_dotenv()

# Get credentials from .env
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")  # Default to 'elastic' if not set

# Connect to Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register the routes
app.register_blueprint(search_routes, url_prefix='/search')

# Store the es connection in the app context
@app.before_request
def before_request():
    g.es = es  # Store Elasticsearch connection in the 'g' object

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
