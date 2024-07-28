import PyPDF2
import pandas as pd
import re
import os

def clean_text(text):
    # Remove any non-printable characters from the text
    return ''.join(c if c.isprintable() else '' for c in text)

def extract_information_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        # Start from the second page (index 1)
        for page_number in range(1, number_of_pages):  
            page = reader.pages[page_number]
            text += page.extract_text()

    # Tisztítsuk meg a kinyert szöveget
    text = clean_text(text)

    general_info = {
        "Szerző": "",
        "Irányító tanár (ok)": "",
        "Év": "",
        "Kivonat": ""
    }

    # Extract author information
    author_match = re.search(r'Candidat\s*[:\-]?\s*([A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\s]+)', text, re.IGNORECASE)
    if author_match:
        author = author_match.group(1).strip()
        author = re.sub(r'\s*Anul\s*absolvirii\s*', '', author).strip()
        general_info["Szerző"] = author

    # Extract supervisor information
    supervisor_match = re.search(r'(?:Coordonator\s*științific|Irányító\s*tanár)\s*[:\-]?\s*([A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\s\.\-]+)', text, re.IGNORECASE)
    if supervisor_match:
        supervisor = supervisor_match.group(1).strip()
        # Remove any unwanted text that might be trailing after the name
        supervisor = re.sub(r'\s*Candidat.*', '', supervisor).strip()
        general_info["Irányító tanár (ok)"] = supervisor

    # Extract year information
    year_match = re.search(r'Anul\s*absolvirii\s*[:\-]?\s*(\d{4})', text, re.IGNORECASE)
    if year_match:
        year = year_match.group(1).strip()
        general_info["Év"] = year

    # Extract abstract information
    abstract_match = re.search(r'Kivonat\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|(?:Kulcsszavak|Keywords|1\.\s*BEVEZETÉS|$))', text, re.IGNORECASE)
    if abstract_match:
        abstract = abstract_match.group(1).strip()
        general_info["Kivonat"] = abstract

    return general_info

def process_pdfs(pdf_dir):
    data = []
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                info = extract_information_from_pdf(pdf_path)
                data.append(info)

    df = pd.DataFrame(data)
    return df

# Process the PDFs in the 'szamteches' directory
szamteches_df = process_pdfs('szamteches')

# Save the extracted information to an Excel file
szamteches_df.to_excel('szamteches_info_extracted.xlsx', index=False)
