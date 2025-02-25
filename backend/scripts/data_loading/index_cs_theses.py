from dotenv import load_dotenv
import os
import json
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

with open("backend\scripts\pdf_processing\cleaned_data.json", "r", encoding="utf-8") as f:
    theses_data = json.load(f)

for i, thesis in enumerate(theses_data, start=1):
    es.index(index="cs_theses", id=i, document=thesis)

print("Data indexed successfully with explicit IDs.")
