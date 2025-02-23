import PyPDF2 
import pandas as pd 
import re
import os

def clean_text(text):
    return ''.join(c if c.isprintable() else '' for c in text)

def extract_information_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        for page_number in range(1, number_of_pages):  
            page = reader.pages[page_number]
            text += page.extract_text()

    text = clean_text(text)

    general_info = {
        "Szerző": "",
        "Irányító tanár (ok)": "",
        "Év": "",
        "Kivonat (magyar)": "",
        "Kivonat (angol)": "",
        "Kulcsszavak (magyar)": "",
        "Kulcsszavak (angol)": ""
    }

    author_match = re.search(r'Candidat\s*[:\-]?\s*([A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\s]+)', text, re.IGNORECASE)
    if author_match:
        author = author_match.group(1).strip()
        author = re.sub(r'\s*Anul\s*absolvirii\s*', '', author).strip()
        general_info["Szerző"] = author

    supervisor_match = re.search(r'(?:Coordonator\s*științific|Irányító\s*tanár)\s*[:\-]?\s*([A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\s\.\-]+)', text, re.IGNORECASE)
    if supervisor_match:
        supervisor = supervisor_match.group(1).strip()
        supervisor = re.sub(r'\s*Candidat.*', '', supervisor).strip()
        general_info["Irányító tanár (ok)"] = supervisor

    year_match = re.search(r'Anul\s*absolvirii\s*[:\-]?\s*(\d{4})', text, re.IGNORECASE)
    if year_match:
        year = year_match.group(1).strip()
        general_info["Év"] = year

    hungarian_abstract_match = re.search(r'Kivonat\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|(?:Kulcsszavak|Keywords|1\.\s*BEVEZETÉS|$))', text, re.IGNORECASE)
    if hungarian_abstract_match:
        hungarian_abstract = hungarian_abstract_match.group(1).strip()
        general_info["Kivonat (magyar)"] = hungarian_abstract

    english_abstract_match = re.search(r'Abstract\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|(?:Keywords|Kulcsszavak|1\.\s*INTRODUCTION|$))', text, re.IGNORECASE)
    if english_abstract_match:
        english_abstract = english_abstract_match.group(1).strip()
        general_info["Kivonat (angol)"] = english_abstract

    hungarian_keywords_match = re.search(r'Kulcsszavak\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|(?:1\.\s*BEVEZETÉS|$)|\s*(?:[A-Z]{1}\.\s*|(?:Abstract|KIVONAT|1\.\s*BEVEZETÉS|$)|\s*Abstrac))', text, re.IGNORECASE)
    if hungarian_keywords_match:
        hungarian_keywords = hungarian_keywords_match.group(1).strip()
        hungarian_keywords = re.sub(r'\s*[\n\r]+\s*', ', ', hungarian_keywords)
        general_info["Kulcsszavak (magyar)"] = hungarian_keywords

    english_keywords_match = re.search(r'Keywords\s*[:\-]?\s*([\s\S]*?)(?:\n{2,}|\n|(?:\b[1-9]\b|Tartalomjegyzék))', text, re.IGNORECASE)
    if english_keywords_match:
        english_keywords = english_keywords_match.group(1).strip()
        english_keywords = re.sub(r'\s*[\n\r]+\s*', ', ', english_keywords)
        general_info["Kulcsszavak (angol)"] = english_keywords

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

szamteches_df = process_pdfs('backend\scripts\pdf_docs\szamteches')

szamteches_df.to_excel('backend\scripts\pdf_processing\szamteches_info_extracted.xlsx', index=False)
