import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")

OLLAMA_API_BASE = "http://localhost:11434/api"
MODEL_NAME = "llama3.2:3b"

OUTPUT_FILE = "backend\scripts\category_extraction\results\abstract_topic_summaries.txt"
LOG_FILE = "backend\scripts\category_extraction\results\processing_log.txt"

def setup_elasticsearch():
    """Setup Elasticsearch connection"""
    es = Elasticsearch(
        "http://localhost:9200",
        basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
    )
    
    if not es.ping():
        raise ConnectionError("Failed to connect to Elasticsearch")
    
    print("✅ Connected to Elasticsearch!")
    return es

def check_ollama_model():
    """Check if Ollama model is available"""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            available_models = [model["name"] for model in models]
            
            if MODEL_NAME in available_models:
                print(f"✅ Ollama model '{MODEL_NAME}' is available!")
                return True
            else:
                print(f"❌ Model '{MODEL_NAME}' not found. Available models: {available_models}")
                print(f"Please run: ollama pull {MODEL_NAME}")
                return False
        else:
            print("❌ Failed to connect to Ollama API")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        print("Make sure Ollama is running: ollama serve")
        return False

def get_all_abstracts(es):
    """Fetch all abstracts from both CS and Informatics indices"""
    abstracts = []
    
    indices = ["cs_theses", "infos_theses"]
    
    for index_name in indices:
        try:
            print(f"📥 Fetching abstracts from {index_name}...")
            
            query = {
                "query": {"match_all": {}},
                "size": 10000,
                "_source": ["author", "year", "abstract", "department", "hash_code"]
            }
            
            response = es.search(index=index_name, body=query)
            documents = response['hits']['hits']
            
            for doc in documents:
                source = doc['_source']
                abstract = source.get('abstract', '').strip()
                
                if abstract and len(abstract) > 50:
                    abstracts.append({
                        'id': doc['_id'],
                        'author': source.get('author', 'Unknown'),
                        'year': source.get('year', 'Unknown'),
                        'abstract': abstract,
                        'department': source.get('department', 'Unknown'),
                        'hash_code': source.get('hash_code', None),
                        'index': index_name
                    })
            
            print(f"✅ Found {len(documents)} documents in {index_name}")
            
        except Exception as e:
            print(f"❌ Error fetching from {index_name}: {e}")
    
    print(f"📊 Total abstracts to process: {len(abstracts)}")
    return abstracts

def generate_topic_summary(abstract, author, year):
    """Generate topic summary using Ollama LLM"""
    prompt = f"""Analyze this academic thesis abstract and extract 3-5 key topic words that best represent the main research areas and technologies discussed. 

Abstract by {author} ({year}):
"{abstract}"

Provide ONLY the key topic words separated by commas, without any explanation or additional text. Focus on:
- Main technologies (e.g., "Machine Learning", "IoT", "React")
- Research domains (e.g., "Computer Vision", "Natural Language Processing")
- Application areas (e.g., "Healthcare", "Education", "Security")

Example output format: Machine Learning, Computer Vision, Healthcare, Python, Deep Learning

Key topics:"""

    try:
        response = requests.post(
            f"{OLLAMA_API_BASE}/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_predict": 50
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            topic_summary = result.get("response", "").strip()
            
            topic_summary = topic_summary.replace('\n', ' ').replace('\r', ' ')
            topic_summary = ' '.join(topic_summary.split())
            
            return topic_summary
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return "Error: API request failed"
            
    except requests.Timeout:
        print("⏰ Request timeout")
        return "Error: Request timeout"
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return f"Error: {str(e)}"

def log_progress(message, log_file):
    """Log progress to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def process_abstracts(abstracts):
    """Process all abstracts and generate topic summaries"""
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Abstract Topic Summarization Log - Started at {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Abstract Topic Summaries - Generated at {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")
    
    log_progress(f"🚀 Starting processing of {len(abstracts)} abstracts", LOG_FILE)
    
    processed_count = 0
    error_count = 0
    
    for i, abstract_data in enumerate(abstracts, 1):
        author = abstract_data['author']
        year = abstract_data['year']
        abstract = abstract_data['abstract']
        department = abstract_data['department']
        
        log_progress(f"📝 Processing {i}/{len(abstracts)}: {author} ({year})", LOG_FILE)
        
        topic_summary = generate_topic_summary(abstract, author, year)
        
        output_line = f"{author} ({year}) [{department.upper()}]: {topic_summary}"
        
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(output_line + '\n')
        
        if "Error:" in topic_summary:
            error_count += 1
            log_progress(f"❌ Error processing {author}: {topic_summary}", LOG_FILE)
        else:
            processed_count += 1
            log_progress(f"✅ Successfully processed {author}", LOG_FILE)
        
        time.sleep(0.5)

        if i % 10 == 0:
            log_progress(f"📊 Progress: {i}/{len(abstracts)} processed ({processed_count} successful, {error_count} errors)", LOG_FILE)
    
    log_progress("🎉 Processing completed!", LOG_FILE)
    log_progress(f"📊 Final results: {processed_count} successful, {error_count} errors", LOG_FILE)
    
    return processed_count, error_count

def main():
    """Main function to run the abstract topic summarization"""
    print("🔬 Abstract Topic Summarizer")
    print("=" * 40)
    
    try:
        if not check_ollama_model():
            return
        
        es = setup_elasticsearch()
        
        abstracts = get_all_abstracts(es)
        
        if not abstracts:
            print("❌ No abstracts found to process")
            return
        
        print(f"\n📋 About to process {len(abstracts)} abstracts")
        print(f"📁 Output file: {OUTPUT_FILE}")
        print(f"📄 Log file: {LOG_FILE}")
        
        user_input = input("\n🤔 Do you want to continue? (y/N): ").lower().strip()
        if user_input != 'y':
            print("❌ Processing cancelled by user")
            return
        
        successful, errors = process_abstracts(abstracts)
        
        print(f"\n🎉 Processing completed!")
        print(f"✅ Successfully processed: {successful}")
        print(f"❌ Errors: {errors}")
        print(f"📁 Results saved to: {OUTPUT_FILE}")
        print(f"📄 Log saved to: {LOG_FILE}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Processing interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
    