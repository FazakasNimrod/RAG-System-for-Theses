# RAG-System-for-Theses

## Project Overview

The "Retrieval Augmented Generation System for Student Diploma Theses" (RAG-System-for-Theses) is designed to automate the extraction of key information from student diploma theses in PDF format. This system utilizes Python and several libraries to extract and process data such as author, supervisor, year, abstract, and keywords, and saves the results in a structured Excel file.

## Features

- **Automated Data Extraction**: Extracts key information from PDFs, including author, supervisor, year, abstract, and keywords.
- **Data Cleaning**: Cleans the extracted text to ensure it is free from non-printable characters and unnecessary data.
- **Regex-Based Parsing**: Uses regular expressions to accurately identify and extract relevant information from the text.
- **Excel Output**: Saves the extracted information into an organized Excel file for easy review and further processing.

## Installation

To run this project locally, you'll need to have Python installed. The required Python packages can be installed using pip:

```bash
pip install PyPDF2 pandas openpyxl
