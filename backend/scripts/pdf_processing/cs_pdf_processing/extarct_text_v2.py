import pdfplumber
import re
import os
import json
import hashlib
from typing import Dict, Optional, List

FIELD_NAMES = {
    "author": "author",
    "supervisor": "supervisor",
    "year": "year",
    "abstract": "abstract",
    "keywords": "keywords",
    "hash_code": "hash_code",
    "department": "department"
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
        print(f"Hiba: {pdf_path} - {str(e)}")
        return None

def extract_info(text: str, pdf_path: str) -> Dict[str, str]:
    """Extract specific information from the cleaned text using regex patterns."""
    info = {value: "" if key != "keywords" else [] for key, value in FIELD_NAMES.items()}
    
    info[FIELD_NAMES["department"]] = "cs"
    
    filename = os.path.basename(pdf_path)
    info[FIELD_NAMES["hash_code"]] = title_to_hash_code(filename)

    # Extract Year
    year_match = re.search(r'\n\s*(20\d{2})\s*\n', text)
    if year_match:
        info[FIELD_NAMES["year"]] = year_match.group(1).strip()
    else:
        year_match = re.search(r'Anul absolvirii:\s*(\d{4})', text, re.IGNORECASE)
        if year_match:
            info[FIELD_NAMES["year"]] = year_match.group(1).strip()

    # Extract Author and Supervisor
    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]
    author_word_count = len(filename_base.split('_'))

    coord_abs_match = re.search(
        r'Coordonator\s+[sșş]tiin[tțţ]ific:\s*Absolvent:\s*\n\s*(.+?)(?:\s*\n\s*(?:Consultant|20\d{2}|$))',
        text, re.IGNORECASE | re.DOTALL
    )
    if coord_abs_match:
        full_content = coord_abs_match.group(1).strip()
        
        lines = full_content.split('\n')
        
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r'^[\s,]+|[\s,]+$', '', line)
            cleaned_line = re.sub(r'\s+', ' ', cleaned_line)
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        
        if len(cleaned_lines) > 1:
            first_line = cleaned_lines[0]
            words = first_line.split()
            if len(words) >= author_word_count:
                author_words = words[-author_word_count:]
                info[FIELD_NAMES["author"]] = " ".join(author_words)
                supervisor_part_first = " ".join(words[:-author_word_count])
                supervisor_parts = [supervisor_part_first] + cleaned_lines[1:]
                info[FIELD_NAMES["supervisor"]] = ", ".join(supervisor_parts)
            else:
                print(f"Warning: Not enough words in first non-empty line '{first_line}' to split based on author word count {author_word_count}")
        elif len(cleaned_lines) == 1:
            cleaned_line = cleaned_lines[0]
            words = cleaned_line.split()
            if len(words) >= author_word_count:
                author_words = words[-author_word_count:]
                info[FIELD_NAMES["author"]] = " ".join(author_words)
                supervisor_words = words[:-author_word_count]
                info[FIELD_NAMES["supervisor"]] = " ".join(supervisor_words)
            else:
                print(f"Warning: Not enough words in line '{cleaned_line}' to split based on author word count {author_word_count}")
        else:
            print(f"Warning: No non-empty lines found in captured content for {pdf_path}")
    else:
        print(f"Warning: Could not match 'Coordonator [sșş]tiin[tțţ]ific: Absolvent:' line in {pdf_path}")
        info[FIELD_NAMES["author"]] = filename_base

    # Extract Abstract
    abstract_match = re.search(
        r'Abstract\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|Keywords|Tartalomjegyzék|$)',
        text, re.IGNORECASE
    )
    if abstract_match:
        info[FIELD_NAMES["abstract"]] = abstract_match.group(1).strip()

    # Extract Keywords
    keywords_match = re.search(
        r'Keywords\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|Tartalomjegyzék|Tartalom|Keywords|1.|$)',
        text, re.IGNORECASE
    )
    if keywords_match:
        keywords_text = keywords_match.group(1).strip()
        keywords_text = re.sub(r'\s*[\n\r]+\s*', ' ', keywords_text).strip()
        keywords_list = [keyword.strip() for keyword in keywords_text.split(',') if keyword.strip()]
        info[FIELD_NAMES["keywords"]] = keywords_list

    return info

def process_pdf(pdf_path: str) -> Dict[str, str]:
    """Process a PDF file and extract required information."""
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        info = {value: "" if key != "keywords" else [] for key, value in FIELD_NAMES.items()}
        info[FIELD_NAMES["department"]] = "cs"
        filename = os.path.basename(pdf_path)
        info[FIELD_NAMES["hash_code"]] = title_to_hash_code(filename)
        info[FIELD_NAMES["author"]] = os.path.splitext(os.path.basename(pdf_path))[0]
        return info
    return extract_info(text, pdf_path)

def process_all_pdfs(folder_path: str) -> List[Dict[str, str]]:
    """Process all PDFs in the specified folder and return a list of extracted data."""
    extracted_data = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {pdf_path}...")
            info = process_pdf(pdf_path)
            extracted_data.append(info)
    
    return extracted_data

def write_to_json(data: List[Dict[str, str]], json_path: str):
    """Write the list of extracted data to a JSON file."""
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    """Main function to process all PDFs in the szamteches folder and write to JSON."""
    folder_path = r"backend\scripts\pdf_docs\szamteches"
    json_path = r"backend\scripts\pdf_processing\cs_pdf_processing\extracted_data.json"

    extracted_data = process_all_pdfs(folder_path)

    write_to_json(extracted_data, json_path)
    print(f"Data from all PDFs written to {json_path}")

if __name__ == "__main__":
    main()
    