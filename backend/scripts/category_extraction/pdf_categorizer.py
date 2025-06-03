"""
PDF Topic Categorizer Script

This script categorizes thesis PDFs based on their abstracts using an LLM.
It reads thesis data from JSON files and outputs categorized results to a text file.

Usage:
    python pdf_categorizer.py

Output:
    Creates 'categorized_theses.txt' with format: "Author, Year, Department - Category"
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
import requests
from pathlib import Path

OLLAMA_API_BASE = "http://localhost:11434/api"
OLLAMA_MODEL = "llama3.2:3b"

CATEGORIES = {
    "1": "Artificial Intelligence & Machine Learning",
    "2": "Web & Mobile Application Development", 
    "3": "IoT, Embedded Systems & Hardware",
    "4": "Healthcare & Bioinformatics",
    "5": "Education Technology & Gamification",
    "6": "Security & Network Systems",
    "7": "Business & Management Systems"
}

SUBCATEGORIES = {
    "1": [
        "Computer Vision & Image Processing",
        "Natural Language Processing", 
        "Neural Networks & Deep Learning",
        "Bot Detection & Security AI",
        "Predictive Analytics & Data Mining"
    ],
    "2": [
        "Web Development (React, Angular, Vue, etc.)",
        "Mobile Apps (Android, iOS, Flutter, React Native)",
        "Progressive Web Applications",
        "Cross-platform Development"
    ],
    "3": [
        "Internet of Things (IoT)",
        "Microcontrollers (Arduino, ESP32, Raspberry Pi)",
        "Sensors & Automation",
        "FPGA & Hardware Design",
        "Robotics & Control Systems"
    ],
    "4": [
        "Medical Imaging & Diagnostics",
        "Health Monitoring Applications",
        "Bioinformatics & Gene Analysis",
        "Telemedicine & Healthcare IT",
        "Rehabilitation & Therapy Systems"
    ],
    "5": [
        "E-learning Platforms",
        "Educational Games & Visualization",
        "Algorithm Teaching Tools",
        "Programming Education",
        "Virtual Tours & 3D Learning"
    ],
    "6": [
        "Cybersecurity & Authentication",
        "Biometric Systems",
        "Blockchain & Cryptocurrency",
        "Network Protocols & Communication",
        "Privacy & Data Protection"
    ],
    "7": [
        "E-commerce & Online Services",
        "ERP & Inventory Management",
        "Project Management Tools",
        "Social Networking Platforms",
        "Event Management Systems"
    ]
}

def check_ollama_connection():
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/tags", timeout=5)
        if response.status_code == 200:
            available_models = response.json().get("models", [])
            model_names = [model["name"] for model in available_models]
            
            if OLLAMA_MODEL in model_names:
                print(f"✓ Connected to Ollama. Using model: {OLLAMA_MODEL}")
                return True
            else:
                print(f"✗ Model {OLLAMA_MODEL} not found. Available models: {model_names}")
                print(f"Please run: ollama pull {OLLAMA_MODEL}")
                return False
        else:
            print("✗ Ollama API not responding properly")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to Ollama: {e}")
        print("Please make sure Ollama is running (ollama serve)")
        return False

def categorize_thesis_with_llm(author: str, year: str, abstract: str, keywords: List[str]) -> str:
    """
    Use LLM to categorize a thesis based on its abstract and keywords.
    
    Args:
        author: Author name
        year: Publication year
        abstract: Thesis abstract
        keywords: List of keywords
        
    Returns:
        Category name as string
    """
    categories_text = "\n".join([f"{num}. {name}" for num, name in CATEGORIES.items()])
    
    keywords_text = ", ".join(keywords) if keywords else "No keywords provided"
    
    prompt = f"""You are an expert in computer science and technology research classification. 

Please categorize the following thesis into ONE of these 7 main categories based on its abstract and keywords:

{categories_text}

THESIS INFORMATION:
Author: {author} ({year})
Keywords: {keywords_text}

Abstract: {abstract}

INSTRUCTIONS:
1. Read the abstract carefully and identify the main research area
2. Consider the keywords as additional context
3. Choose the MOST APPROPRIATE category from the 7 options above
4. Respond with ONLY the category number and name in this exact format: "X. Category Name"
5. Do not provide explanations, just the category

Your response:"""

    try:
        response = requests.post(
            f"{OLLAMA_API_BASE}/generate",
            json={
                "model": OLLAMA_MODEL,
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
            llm_response = result.get("response", "").strip()
            
            for num, category_name in CATEGORIES.items():
                if num in llm_response and category_name.lower() in llm_response.lower():
                    return category_name
                elif category_name.lower() in llm_response.lower():
                    return category_name
            
            category_match = re.search(r'(\d+)\.', llm_response)
            if category_match:
                category_num = category_match.group(1)
                if category_num in CATEGORIES:
                    return CATEGORIES[category_num]
            
            print(f"Warning: Could not parse LLM response for {author}: '{llm_response}'")
            return "Web & Mobile Application Development"
            
        else:
            print(f"Error from Ollama API: {response.status_code}")
            return "Web & Mobile Application Development"
            
    except Exception as e:
        print(f"Error calling LLM for {author}: {e}")
        return "Web & Mobile Application Development"

def load_thesis_data() -> List[Dict]:
    """Load thesis data from JSON files."""
    all_theses = []
    
    data_files = [
        "backend/scripts/pdf_processing/cs_pdf_processing/cleaned_data.json",
        "backend/scripts/pdf_processing/info_pdf_processing/cleaned_infos_data.json"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_theses.extend(data)
                    print(f"✓ Loaded {len(data)} theses from {file_path}")
            except Exception as e:
                print(f"✗ Error loading {file_path}: {e}")
        else:
            print(f"✗ File not found: {file_path}")
    
    return all_theses

def clean_author_name(author: str) -> str:
    """Clean and format author name."""
    if not author:
        return "Unknown Author"
    
    cleaned = re.sub(r'\s+', ' ', author.strip())
    
    return cleaned

def main():
    """Main function to categorize all theses."""
    print("🔍 PDF Topic Categorizer")
    print("=" * 50)
    
    if not check_ollama_connection():
        print("\n❌ Cannot proceed without Ollama connection.")
        print("Please start Ollama and ensure the required model is available.")
        return
    
    print("\n📚 Loading thesis data...")
    theses = load_thesis_data()
    
    if not theses:
        print("❌ No thesis data found. Please check the data file paths.")
        return
    
    print(f"✓ Found {len(theses)} theses to categorize")
    
    results = []
    processed = 0
    
    print(f"\n🤖 Starting categorization with {OLLAMA_MODEL}...")
    print("This may take a few minutes...")
    
    for i, thesis in enumerate(theses, 1):
        author = clean_author_name(thesis.get('author', 'Unknown'))
        year = thesis.get('year', 'Unknown')
        abstract = thesis.get('abstract', '')
        keywords = thesis.get('keywords', [])
        
        department = thesis.get('department', 'unknown')
        if department == 'cs':
            dept_short = 'cs'
        elif department == 'informatics':
            dept_short = 'info'
        else:
            dept_short = 'unknown'
        
        if not abstract:
            print(f"⚠️  Skipping {author}, {year}, {dept_short} - No abstract available")
            continue
        
        print(f"Processing {i}/{len(theses)}: {author}, {year}, {dept_short}")
        
        category = categorize_thesis_with_llm(author, str(year), abstract, keywords)
        
        result_line = f"{author}, {year}, {dept_short} - {category}"
        results.append(result_line)
        
        processed += 1
        
        time.sleep(0.5)
        
        if processed % 10 == 0:
            print(f"✓ Processed {processed} theses...")
    
    output_file = "backend\scripts\category_extraction\results\categorized_theses.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(result + '\n')
        
        print(f"\n✅ Successfully categorized {len(results)} theses!")
        print(f"📄 Results saved to: {output_file}")
        
        print(f"\n📊 Category Distribution:")
        category_counts = {}
        for result in results:
            category = result.split(" - ")[-1]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} theses")
            
    except Exception as e:
        print(f"❌ Error writing results: {e}")

if __name__ == "__main__":
    main()