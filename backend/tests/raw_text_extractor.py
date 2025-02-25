import pdfplumber
import os

def extract_raw_text(pdf_path):
    """Extract raw text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            raw_text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    raw_text += page_text + '\n'
        return raw_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return None

if __name__ == "__main__":
    pdf_path = r"backend\scripts\pdf_docs\szamteches\Bálint_Adolf.pdf"
    
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = f"{base_name}.txt"
    
    raw_text = extract_raw_text(pdf_path)
    if raw_text:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(raw_text)
        print(f"Raw text saved to {output_path}")
        