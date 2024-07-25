import PyPDF2
import pandas as pd
import re
import os

def clean_text(text):
    # Tisztítsuk meg a szöveget az illegális karakterektől
    return ''.join(c if c.isprintable() else '' for c in text)

def extract_author_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            text += page.extract_text()

    # Tisztítsuk meg a kinyert szöveget
    text = clean_text(text)

    # Extract author information using "Candidat" and clean up unwanted parts
    author_match = re.search(r'Candidat\s*[:\-]?\s*([A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\s]+)', text, re.IGNORECASE)
    if author_match:
        author = author_match.group(1).strip()
        # Remove any trailing non-name text like "Anul absolvirii"
        author = re.sub(r'\s*Anul\s*absolvirii\s*', '', author).strip()
        return author

    return ""

def process_pdfs_for_authors(pdf_dir):
    data = []
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                author = extract_author_from_pdf(pdf_path)
                data.append({"Szerző": author})

    df = pd.DataFrame(data)
    return df

# Process the PDFs in the 'szamteches' directory
szamteches_df = process_pdfs_for_authors('szamteches')

# Save the extracted information to an Excel file
szamteches_df.to_excel('szamteches_authors_extracted.xlsx', index=False)
