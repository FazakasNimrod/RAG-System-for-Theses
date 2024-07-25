import PyPDF2
import pandas as pd
import re
import os

def extract_information_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            text += page.extract_text()

    general_info = {
        "Általános": {"Szerző": "", "Irányító tanár (ok)": "", "Év": ""},
        "HU": {"cím": "", "kivonat": "", "kulcsszavak": ""}
    }

    # Extract general information
    author_match = re.search(r'(?:Szerző|Absolvent(?:ă)?)\s*:\s*(.*)', text, re.IGNORECASE)
    supervisor_match = re.search(r'(?:Irányító tanár(?:ok)?|Coordonator științific)\s*:\s*(.*)', text, re.IGNORECASE)
    year_match = re.search(r'\b(\d{4})\b', text)

    if author_match:
        general_info["Általános"]["Szerző"] = author_match.group(1).strip()
    if supervisor_match:
        general_info["Általános"]["Irányító tanár (ok)"] = supervisor_match.group(1).strip()
    if year_match:
        general_info["Általános"]["Év"] = year_match.group(1).strip()

    # Extract Hungarian information
    hu_title_match = re.search(r'(?:HU: cím|Hőkövető robot tervezése és megvalósítása)\s*(.*)', text, re.IGNORECASE)
    hu_abstract_match = re.search(r'Kivonat\s*([\s\S]*?)\s*(?:Kulcsszavak|Keywords)', text, re.IGNORECASE)
    hu_keywords_match = re.search(r'Kulcsszavak\s*:\s*(.*)', text, re.IGNORECASE)

    if hu_title_match:
        general_info["HU"]["cím"] = hu_title_match.group(1).strip()
    if hu_abstract_match:
        general_info["HU"]["kivonat"] = hu_abstract_match.group(1).strip()
    if hu_keywords_match:
        general_info["HU"]["kulcsszavak"] = hu_keywords_match.group(1).strip()

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
szamteches_df.to_excel('szamteches_extracted_information.xlsx', index=False)
