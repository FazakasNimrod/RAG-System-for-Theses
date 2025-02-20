import pdfplumber
import re
import os
import json
from typing import Dict, Optional, List

# Constants for field names (updated to English keys for JSON output)
FIELD_NAMES = {
    "author": "author",
    "supervisor": "supervisor",
    "year": "year",
    "abstract": "abstract",
    "keywords": "keywords"
}

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

    # Extract Year (year)
    year_match = re.search(r'\n\s*(20\d{2})\s*\n', text)
    if year_match:
        info[FIELD_NAMES["year"]] = year_match.group(1).strip()
    else:
        year_match = re.search(r'Anul absolvirii:\s*(\d{4})', text, re.IGNORECASE)
        if year_match:
            info[FIELD_NAMES["year"]] = year_match.group(1).strip()

    # Get the number of words in the author's name from the filename
    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]  # e.g., "Pál_Andor"
    author_word_count = len(filename_base.split('_'))  # e.g., 2 for "Pál_Andor"

    # Extract all content between "Coordonator" and "20\d{2}" or section break
    coord_abs_match = re.search(
        r'Coordonator\s+[sșş]tiin[tțţ]ific:\s*Absolvent:\s*\n\s*(.+?)(?:\s*\n\s*(?:Consultant|20\d{2}|$))',
        text, re.IGNORECASE | re.DOTALL
    )
    if coord_abs_match:
        full_content = coord_abs_match.group(1).strip()  # e.g., ", ,\nDr. Szabó László Zsolt Pál Andor"
        
        # Split into lines first
        lines = full_content.split('\n')  # Split on newlines without stripping yet
        
        # Clean each line and filter out empty results
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r'^[\s,]+|[\s,]+$', '', line)  # Remove leading/trailing spaces and commas
            cleaned_line = re.sub(r'\s+', ' ', cleaned_line)  # Collapse multiple spaces into single spaces
            if cleaned_line:  # Only keep non-empty lines after cleaning
                cleaned_lines.append(cleaned_line)
        
        # Determine if multi-line and extract accordingly
        if len(cleaned_lines) > 1:
            # Multi-line case: Extract author from the first non-empty line
            first_line = cleaned_lines[0]  # e.g., "Dr. Szabó László Zsolt Pál Andor"
            words = first_line.split()
            if len(words) >= author_word_count:
                author_words = words[-author_word_count:]  # Last n words from first non-empty line
                info[FIELD_NAMES["author"]] = " ".join(author_words)
                supervisor_part_first = " ".join(words[:-author_word_count])  # Supervisor from first line
                # Combine all supervisor parts from all cleaned lines
                supervisor_parts = [supervisor_part_first] + cleaned_lines[1:]
                info[FIELD_NAMES["supervisor"]] = ", ".join(supervisor_parts)
            else:
                print(f"Warning: Not enough words in first non-empty line '{first_line}' to split based on author word count {author_word_count}")
        elif len(cleaned_lines) == 1:
            # Single-line case: Use the cleaned content as is
            cleaned_line = cleaned_lines[0]  # e.g., "Conf. dr. ing. Bakó László Bakó József"
            words = cleaned_line.split()
            if len(words) >= author_word_count:
                author_words = words[-author_word_count:]  # Last n words
                info[FIELD_NAMES["author"]] = " ".join(author_words)
                supervisor_words = words[:-author_word_count]  # All but last n
                info[FIELD_NAMES["supervisor"]] = " ".join(supervisor_words)
            else:
                print(f"Warning: Not enough words in line '{cleaned_line}' to split based on author word count {author_word_count}")
        else:
            print(f"Warning: No non-empty lines found in captured content for {pdf_path}")
    else:
        print(f"Warning: Could not match 'Coordonator [sșş]tiin[tțţ]ific: Absolvent:' line in {pdf_path}")

    # Extract Abstract (abstract)
    abstract_match = re.search(
        r'Abstract\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|Keywords|Tartalomjegyzék|$)',
        text, re.IGNORECASE
    )
    if abstract_match:
        info[FIELD_NAMES["abstract"]] = abstract_match.group(1).strip()

    # Extract Keywords (keywords) as a list
    keywords_match = re.search(
        r'Keywords\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|Tartalomjegyzék|Tartalom|Keywords|$)',
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
        return {value: "" if key != "keywords" else [] for key, value in FIELD_NAMES.items()}
    return extract_info(text, pdf_path)

def process_all_pdfs(folder_path: str) -> List[Dict[str, str]]:
    """Process all PDFs in the specified folder and return a list of extracted data."""
    extracted_data = []
    
    # Iterate through all files in the folder
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
    json_path = r"backend\scripts\pdf_processing\extracted_data.json"

    # Process all PDFs in the folder
    extracted_data = process_all_pdfs(folder_path)

    # Write the extracted data to JSON
    write_to_json(extracted_data, json_path)
    print(f"Data from all PDFs written to {json_path}")

if __name__ == "__main__":
    main()