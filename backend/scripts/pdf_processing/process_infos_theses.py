import pdfplumber
import re
import os
import json
import hashlib
from typing import Dict, Optional, List
from keybert import KeyBERT

INPUT_FOLDER = "backend\scripts\pdf_docs\infos"
OUTPUT_JSON = "backend\scripts\pdf_processing\extracted_infos_data.json"
CLEANED_OUTPUT_JSON = "backend\scripts\pdf_processing\cleaned_infos_data.json"

FIELD_NAMES = {
    "author": "author",
    "supervisor": "supervisor",
    "year": "year",
    "abstract": "abstract",
    "keywords": "keywords",
    "department": "department",
    "hash_code": "hash_code"
}

def title_to_hash_code(title):
    """
    Convert a title to a unique 10-digit hash code
    
    Args:
        title (str): The title of the PDF
    
    Returns:
        int: A unique 10-digit hash code representation of the title
    """
    def normalize_title(title):
        normalized = title.lower()
        
        normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    normalized_title = normalize_title(title)
    
    hash_object = hashlib.sha256(normalized_title.encode())
 
    full_hash = int(hash_object.hexdigest(), 16)
    
    ten_digit_hash = full_hash % 10000000000
    
    return ten_digit_hash

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """Extract raw text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            return text
    except Exception as e:
        print(f"Error: {pdf_path} - {str(e)}")
        return None

def extract_author_from_filename(pdf_path: str) -> str:
    """Extract author from filename following pattern LastName_FirstName_Diplomadolgozat_YYYY.pdf."""
    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]
    filename_parts = filename_base.split('_')
    
    if len(filename_parts) >= 2:
        author_name = f"{filename_parts[0]} {filename_parts[1]}"
        return author_name
    return ""

def extract_author_and_supervisor(text: str) -> tuple:
    """
    Extract author and supervisor information from the specific pattern:
    "Témavezetők: Végzős hallgató: 
    Dr.Osztián Erika, Balázs Endre 
    Egyetemi adjunktus..."
    or equivalent patterns in different languages.
    """
    patterns = [
        r'Témavezet[őo][k]?\s*:\s*Végzős hallgató\s*:\s*\n((?:.+\n)+?)(?:20\d{2}|$)',
        r'Coordonator[i]?\s*[sșş]tiin[tțţ]ific[i]?\s*:\s*Absolvent\s*:\s*\n((?:.+\n)+?)(?:20\d{2}|$)',
        r'Scientific advisor[s]?\s*:\s*Student\s*:\s*\n((?:.+\n)+?)(?:20\d{2}|$)'
    ]
    
    for pattern in patterns:
        matches = re.search(pattern, text, re.IGNORECASE)
        if matches:
            section_content = matches.group(1).strip()
            
            lines = section_content.strip().split('\n')
            
            if lines:
                first_line = lines[0].strip()

                parts = first_line.split(',')
                
                if len(parts) > 0:
                    author = parts[-1].strip()
                    supervisors = [p.strip() for p in parts[:-1]]
                    
                    for line in lines[1:]:
                        line = line.strip()
                        if line and not any(title in line.lower() for title in ['egyetemi', 'adjunktus', 'tanársegéd', 'lector', 'asistent', 'professor']):
                            supervisors.append(line)
                    
                    cleaned_supervisors = clean_supervisors(supervisors)
                    
                    return author, cleaned_supervisors
    
    return None, None

def clean_supervisors(supervisors_list):
    """Clean supervisor names by removing academic titles and trailing commas."""
    titles_to_remove = [
        r'Dr\.', r'Conf\.', r'Ș\.l\.', r'ing\.', r'Prof\.', r'habil\.',
        r'conferențiar universitar', r'Șef\. lucr\.', r'ing', r'Drd\.',
        r'Conferentiar universitar', r'Lector universitar', r'Asistent universitar',
        r'Asistent Universitar', r'Egyetemi adjunktus', r'Egyetemi tanársegéd',
        r'Phd\.', r'PhD\.', r'Ph\.D\.', r'Docens'
    ]
    
    cleaned_supervisors = []
    
    for supervisor in supervisors_list:
        cleaned = supervisor
        for title in titles_to_remove:
            cleaned = re.sub(title, '', cleaned, flags=re.IGNORECASE)
        
        cleaned = cleaned.rstrip(',')
        
        cleaned = ' '.join(cleaned.split())
        
        if cleaned:
            cleaned_supervisors.append(cleaned)
    
    return cleaned_supervisors

def extract_info(text: str, pdf_path: str) -> Dict[str, str]:
    """Extract specific information from the cleaned text using regex patterns."""
    info = {value: "" if key != "keywords" else [] for key, value in FIELD_NAMES.items()}
    
    info[FIELD_NAMES["department"]] = "informatics"
    
    filename = os.path.basename(pdf_path)
    info[FIELD_NAMES["hash_code"]] = title_to_hash_code(filename)
    
    author, supervisors = extract_author_and_supervisor(text)
    
    if author:
        info[FIELD_NAMES["author"]] = author
    else:
        info[FIELD_NAMES["author"]] = extract_author_from_filename(pdf_path)
    
    if supervisors:
        info[FIELD_NAMES["supervisor"]] = supervisors

    year_match = re.search(r'\n\s*(20\d{2})\s*\n', text)
    if year_match:
        info[FIELD_NAMES["year"]] = year_match.group(1).strip()
    else:
        year_match = re.search(r'Anul absolvirii:\s*(\d{4})', text, re.IGNORECASE)
        if year_match:
            info[FIELD_NAMES["year"]] = year_match.group(1).strip()
        else:
            filename = os.path.basename(pdf_path)
            year_match = re.search(r'_(\d{4})\.pdf$', filename)
            if year_match:
                info[FIELD_NAMES["year"]] = year_match.group(1).strip()

    abstract_patterns = [
    r'\bAbstract\b\s*[:\-]?\s*([\s\S]*?)(?=Keywords|Kulcsszavak|Cuvinte cheie|Tartalomjegyzék|Rezumat|Kivonat|$)',
    r'\bKivonat\b\s*[:\-]?\s*([\s\S]*?)(?=Kulcsszavak|Keywords|Rezumat|Abstract|$)',
    r'\bRezumat\b\s*[:\-]?\s*([\s\S]*?)(?=Cuvinte cheie|Keywords|Kulcsszavak|Abstract|Kivonat|$)'
    ]

    for pattern in abstract_patterns:
        abstract_match = re.search(pattern, text, re.IGNORECASE)
        if abstract_match:
            abstract_text = abstract_match.group(1).strip()
            if len(abstract_text) > 30: 
                abstract_text = clean_abstract(abstract_text)
                info[FIELD_NAMES["abstract"]] = abstract_text
                break

    keyword_patterns = [
        r'Keywords\s*[:\-]?\s*([\s\S]*?)(?=\n{2,}|Introduction|Tartalomjegyzék|Tartalom|Table of contents|1\.|$)'
    ]
    
    for pattern in keyword_patterns:
        keywords_match = re.search(pattern, text, re.IGNORECASE)
        if keywords_match:
            keywords_text = keywords_match.group(1).strip()
            keywords_text = re.sub(r'\s*[\n\r]+\s*', ' ', keywords_text)
            
            if ',' in keywords_text:
                keywords = [k.strip() for k in keywords_text.split(',')]
            elif ';' in keywords_text:
                keywords = [k.strip() for k in keywords_text.split(';')]
            else:
                keywords = re.split(r'\s{2,}|\t', keywords_text)
                
            keywords = [k for k in keywords if k]
            
            if keywords:
                info[FIELD_NAMES["keywords"]] = keywords
                break

    return info

def clean_abstract(abstract_str):
    """Clean and format abstract text."""
    if not abstract_str:
        return ""
    
    cleaned = abstract_str.replace('\n', ' ')
    
    cleaned = re.sub(r'\.([A-Z])', r'. \1', cleaned)
    
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    cleaned = cleaned.strip()
    
    return cleaned

def clean_hyphen_space(obj):
    """Recursively clean unwanted hyphen-space patterns."""
    if isinstance(obj, str):
        return obj.replace('- ', '')
    elif isinstance(obj, list):
        return [clean_hyphen_space(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_hyphen_space(value) for key, value in obj.items()}
    else:
        return obj

def process_pdf(pdf_path: str) -> Dict[str, str]:
    """Process a PDF file and extract required information."""
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        info = {value: "" if key != "keywords" else [] for key, value in FIELD_NAMES.items()}
        info[FIELD_NAMES["author"]] = extract_author_from_filename(pdf_path)
        info[FIELD_NAMES["department"]] = "informatics"
        filename = os.path.basename(pdf_path)
        info[FIELD_NAMES["hash_code"]] = title_to_hash_code(filename)
        return info
    
    return extract_info(text, pdf_path)

def generate_keywords(abstract_str, num_keywords=4, max_length=25):
    """Generate keywords from abstract when they're not available."""
    if not abstract_str:
        return []
    
    kw_model = KeyBERT()
    
    keywords = kw_model.extract_keywords(
        abstract_str,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=num_keywords * 2,
        use_mmr=True,
        diversity=0.7
    )
    
    selected_keywords = []
    seen_roots = set()
    
    for keyword, _ in keywords:
        if len(keyword) > max_length:
            continue
        if not keyword.strip():
            continue
        root = keyword.split()[0].lower()
        if root not in seen_roots and len(selected_keywords) < num_keywords:
            selected_keywords.append(keyword)
            seen_roots.add(root)
    
    return selected_keywords

def clean_data(data):
    """Clean and enhance the extracted data."""
    for thesis in data:
        if 'year' in thesis and isinstance(thesis['year'], str) and thesis['year'].isdigit():
            thesis['year'] = int(thesis['year'])
        
        if 'abstract' in thesis and thesis['abstract']:
            thesis['abstract'] = clean_abstract(thesis['abstract'])
        
        if ('keywords' not in thesis or not thesis['keywords']) and 'abstract' in thesis:
            thesis['keywords'] = generate_keywords(thesis['abstract'])
    
    data = clean_hyphen_space(data)
    
    return data

def main():
    """Main function to process all PDFs in the informatics folder and write to JSON."""
    extracted_data = []
    
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Processing {pdf_path}...")
            info = process_pdf(pdf_path)
            extracted_data.append(info)
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)
    
    cleaned_data = clean_data(extracted_data)
    
    with open(CLEANED_OUTPUT_JSON, 'w', encoding='utf-8') as json_file:
        json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Data extraction complete. Raw data written to {OUTPUT_JSON}")
    print(f"Cleaned data written to {CLEANED_OUTPUT_JSON}")

if __name__ == "__main__":
    main()
    