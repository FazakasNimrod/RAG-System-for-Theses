from flask import Flask, g
from flask_cors import CORS
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from routes import search_routes

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

app = Flask(__name__)

CORS(app)

app.register_blueprint(search_routes, url_prefix='/search')

@app.before_request
def before_request():
    g.es = es

if __name__ == '__main__':
    app.run(debug=True)
