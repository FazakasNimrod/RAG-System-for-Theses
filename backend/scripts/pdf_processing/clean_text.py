import json
import re

input_file = 'backend\scripts\pdf_processing\extracted_data.json'
output_file = 'backend\scripts\pdf_processing\cleaned_data.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

titles_to_remove = [
    r'Dr\.', r'Conf\.', r'Ș\.l\.', r'ing\.', r'Prof\.', r'habil\.',
    r'conferențiar universitar', r'Șef\. lucr\.', r'ing'
]

def clean_supervisors(supervisor_str):
    supervisor_str = re.sub(r',,+', ',', supervisor_str).strip(',')
    
    supervisors = [s.strip() for s in supervisor_str.split(',')]
    
    cleaned_supervisors = []
    for supervisor in supervisors:
        cleaned = supervisor
        for title in titles_to_remove:
            cleaned = re.sub(title, '', cleaned, flags=re.IGNORECASE)
        cleaned = ' '.join(cleaned.split())
        if cleaned:
            cleaned_supervisors.append(cleaned)
    
    return cleaned_supervisors

def clean_abstract(abstract_str):
    cleaned = abstract_str.replace('\n', ' ')
    cleaned = ' '.join(cleaned.split())
    return cleaned

def clean_hyphen_space(obj):
    if isinstance(obj, str):
        return obj.replace('- ', '')
    elif isinstance(obj, list):
        return [clean_hyphen_space(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_hyphen_space(value) for key, value in obj.items()}
    else:
        return obj

def clean_keywords(keywords_list):
    if keywords_list and isinstance(keywords_list, list) and len(keywords_list) > 0:
        last_keyword = keywords_list[-1]
        if last_keyword.endswith('.'):
            keywords_list[-1] = last_keyword.rstrip('.')
    return keywords_list

for thesis in data:
    if 'supervisor' in thesis:
        thesis['supervisor'] = clean_supervisors(thesis['supervisor'])
    
    if 'abstract' in thesis:
        thesis['abstract'] = clean_abstract(thesis['abstract'])
    
    if 'keywords' in thesis:
        thesis['keywords'] = clean_keywords(thesis['keywords'])

data = clean_hyphen_space(data)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Refactored JSON saved to {output_file}")
