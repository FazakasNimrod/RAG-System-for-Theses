import json
import re
import os
import logging
from typing import Dict, List, Any, Set, Tuple
from keybert import KeyBERT
from collections import Counter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clean_text_infos_extra.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Input and output file paths
INPUT_FILE = "backend/scripts/pdf_processing/info_pdf_processing/cleaned_infos_data.json"
OUTPUT_FILE = "backend/scripts/pdf_processing/info_pdf_processing/cleaned_infos_data_extra.json"

# Academic titles and positions to remove from author names
ACADEMIC_TITLES = [
    r'Dr\.?', r'dr\.?', r'Prof\.?', r'prof\.?', r'Conf\.?', r'conf\.?', 
    r'Ș\.l\.?', r'ing\.?', r'habil\.?', r'Drd\.?', r'PhD\.?', r'Ph\.D\.?'
]

ACADEMIC_POSITIONS = [
    r'Tanársegéd', r'tanársegéd', r'Egyetemi\s+docens', r'egyetemi\s+docens',
    r'Egyetemi\s+adjunktus', r'egyetemi\s+adjunktus', r'Egyetemi\s+tanársegéd',
    r'egyetemi\s+tanársegéd', r'Conferențiar\s+universitar', r'conferențiar\s+universitar',
    r'Asistent\s+universitar', r'asistent\s+universitar', r'Lector\s+universitar',
    r'lector\s+universitar', r'Șef\.\s*lucr\.?', r'Docens', r'docens',
    r'Associate\s+[Pp]rofessor', r'Assistant\s+[Pp]rofessor', r'Lecturer'
]

# Patterns that should not be in supervisor or author names
INVALID_NAME_PATTERNS = [
    r'Informatică\s+[IVX]+',
    r'Diplom[aă]',
    r'Student',
    r'Végzős',
    r'Absolvent',
    r'LUCRARE',
    r'THESIS',
    r'DIPLOMA',
    r'BACHELOR',
    r'Faculty',
    r'University',
    r'Universitat',
    r'\d{4}'  # Years
]

def load_data(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {filepath}: {e}")
        return []

def save_data(data: List[Dict[str, Any]], filepath: str) -> None:
    """Save JSON data to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Data successfully saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")

def extract_names(text: str) -> List[str]:
    """
    Extract potential person names from text using patterns.
    Looks for sequences of capitalized words that might be names.
    """
    # Look for capitalized word sequences that could be names
    # Hungarian/Romanian names often have 2-3 parts, sometimes with hyphens
    name_pattern = r'([A-ZÁÉÍÓÖŐÚÜŰȘȚŢĂ][a-záéíóöőúüűșțţă]+(?:[-\s]+[A-ZÁÉÍÓÖŐÚÜŰȘȚŢĂ][a-záéíóöőúüűșțţă]+){1,3})'
    return re.findall(name_pattern, text)

def remove_academic_prefixes(name: str) -> str:
    """Remove academic titles and positions from the beginning of a name."""
    original_name = name
    
    # Create a combined pattern for academic titles and positions at the beginning
    prefix_patterns = []
    for title in ACADEMIC_TITLES:
        prefix_patterns.append(f"^{title}\\s+")
    for position in ACADEMIC_POSITIONS:
        prefix_patterns.append(f"^{position}\\s+")
    
    combined_pattern = "|".join(prefix_patterns)
    
    # Remove prefixes while they exist (for multiple titles)
    prev_name = ""
    while prev_name != name:
        prev_name = name
        name = re.sub(combined_pattern, "", name, flags=re.IGNORECASE)
    
    # Remove commas
    name = name.replace(",", "")
    
    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    
    if name != original_name:
        logger.info(f"Removed academic prefixes: '{original_name}' -> '{name}'")
    
    return name

def is_valid_name(name: str) -> bool:
    """Check if a string is a valid person name."""
    # Check for invalid patterns
    for pattern in INVALID_NAME_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return False
    
    # Basic validation: must be 2-4 words, all capitalized
    words = name.split()
    if len(words) < 2 or len(words) > 4:
        return False
    
    # All words in a name should be capitalized
    if not all(word[0].isupper() for word in words if word):
        return False
    
    return True

def build_name_frequency_map(data: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Build a frequency map of all names (authors and supervisors) 
    to identify common names and potential supervisors.
    """
    name_counter = Counter()
    
    # Extract names from author fields
    for thesis in data:
        if "author" in thesis and thesis["author"]:
            # Split complex author names
            author = thesis["author"]
            author = remove_academic_prefixes(author)
            
            # Check for multi-part author names
            if len(author.split()) >= 4:
                potential_names = extract_names(author)
                for name in potential_names:
                    if is_valid_name(name):
                        name_counter[name] += 1
            else:
                if is_valid_name(author):
                    name_counter[author] += 1
        
        # Extract names from supervisor fields
        if "supervisor" in thesis and thesis["supervisor"]:
            supervisors = thesis["supervisor"]
            if isinstance(supervisors, str):
                supervisors = [supervisors]
            
            for supervisor in supervisors:
                supervisor = remove_academic_prefixes(supervisor)
                # Split complex supervisor strings
                potential_names = extract_names(supervisor)
                for name in potential_names:
                    if is_valid_name(name):
                        name_counter[name] += 1
    
    return name_counter

def identify_supervisors(name_freq_map: Dict[str, int], threshold: int = 3) -> Set[str]:
    """
    Identify likely supervisors based on frequency.
    Supervisors tend to appear multiple times across theses.
    """
    supervisors = set()
    for name, count in name_freq_map.items():
        if count >= threshold:
            supervisors.add(name)
    
    logger.info(f"Identified {len(supervisors)} potential supervisors based on frequency")
    return supervisors

def separate_author_supervisor(text: str, known_supervisors: Set[str]) -> Tuple[str, List[str]]:
    """
    Separate a text that might contain both author and supervisor names.
    Returns (author, [supervisors])
    """
    if not text:
        return "", []
    
    # First, remove academic prefixes
    cleaned_text = remove_academic_prefixes(text)
    
    # Extract potential names
    potential_names = extract_names(cleaned_text)
    
    # Check each name against known supervisors
    author = ""
    supervisors = []
    remaining_names = []
    
    for name in potential_names:
        if name in known_supervisors:
            supervisors.append(name)
        else:
            remaining_names.append(name)
    
    # If we found supervisors but no remaining names, try a different approach
    if supervisors and not remaining_names:
        # Try splitting the original text
        words = cleaned_text.split()
        first_half = " ".join(words[:len(words)//2])
        second_half = " ".join(words[len(words)//2:])
        
        # Check which half contains supervisor names
        first_half_supervisors = [name for name in potential_names if name in first_half and name in known_supervisors]
        if first_half_supervisors:
            # First half has supervisors, second half might be author
            author = second_half
        else:
            # Second half might have supervisors, first half might be author
            author = first_half
    elif not supervisors and len(remaining_names) >= 2:
        # If we have multiple names but no identified supervisors,
        # assume the last name is the author
        author = remaining_names[-1]
        for name in remaining_names[:-1]:
            if is_valid_name(name):
                supervisors.append(name)
    elif not supervisors and len(remaining_names) == 1:
        # Only one name found, assume it's the author
        author = remaining_names[0]
    else:
        # We have both supervisors and remaining names
        # Assume the name that's not a supervisor is the author
        if remaining_names:
            author = remaining_names[-1]
    
    # If we still don't have an author but have original text
    if not author and cleaned_text:
        # Try to extract the last capitalized name pattern
        name_matches = list(re.finditer(r'([A-ZÁÉÍÓÖŐÚÜŰȘȚŢĂ][a-záéíóöőúüűșțţă]+(?:[-\s]+[A-ZÁÉÍÓÖŐÚÜŰȘȚŢĂ][a-záéíóöőúüűșțţă]+){1,3})', cleaned_text))
        if name_matches:
            author = name_matches[-1].group(0)
    
    return author.strip(), supervisors

def clean_supervisor_list(supervisors: List[str]) -> List[str]:
    """Clean a list of supervisors by removing invalid entries and duplicates."""
    if not supervisors:
        return []
    
    valid_supervisors = []
    seen = set()
    
    for supervisor in supervisors:
        # Skip empty supervisors
        if not supervisor or supervisor.strip() == "":
            continue
        
        # Remove academic prefixes
        cleaned = remove_academic_prefixes(supervisor)
        
        # Skip invalid patterns
        if any(re.search(pattern, cleaned, re.IGNORECASE) for pattern in INVALID_NAME_PATTERNS):
            logger.info(f"Removing invalid supervisor: '{supervisor}'")
            continue
        
        # Skip if not a valid name after cleaning
        if not is_valid_name(cleaned):
            continue
        
        # Skip duplicates
        if cleaned in seen:
            continue
        
        seen.add(cleaned)
        valid_supervisors.append(cleaned)
    
    return valid_supervisors

def fix_abstract_with_keybert(text: str, kw_model: KeyBERT) -> str:
    """
    Use KeyBERT to identify potential issues with the text and fix them.
    This helps with:
    1. Stuck words where spaces are missing
    2. Identifying important concepts that might be misformatted
    """
    if not text or len(text) < 50:  # Skip very short texts
        return text
    
    # First apply basic regex fix for camelCase
    text = fix_sticked_words(text)
    
    # Extract keywords to identify important concepts
    keywords = kw_model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 2), 
        stop_words='english',
        use_mmr=True,
        diversity=0.5,
        top_n=10
    )
    
    # Look for potential issues with the extracted keywords
    for keyword, _ in keywords:
        # Check if keyword contains unusual capitalization patterns
        if re.search(r'[a-z][A-Z]', keyword):
            parts = re.split(r'(?<=[a-z])(?=[A-Z])', keyword)
            fixed_keyword = ' '.join(parts)
            # Replace all occurrences in the text
            text = text.replace(keyword, fixed_keyword)
            logger.info(f"KeyBERT fixed: '{keyword}' -> '{fixed_keyword}'")
    
    return text

def fix_sticked_words(text: str) -> str:
    """
    Fix words that have been incorrectly joined together in the text.
    Uses heuristics to identify and separate these cases.
    """
    if not text:
        return text
    
    # Regular expression to find camelCase patterns (lowercase followed by uppercase)
    pattern = r'([a-z])([A-Z])'
    
    # Add a space between the matched characters
    fixed_text = re.sub(pattern, r'\1 \2', text)
    
    # If changes were made, log them
    if fixed_text != text:
        # Log only a sample of changes to keep log files manageable
        sample = next((i for i, (c1, c2) in enumerate(zip(text, fixed_text)) if c1 != c2), -1)
        if sample >= 0:
            context_start = max(0, sample - 20)
            context_end = min(len(text), sample + 20)
            context = text[context_start:context_end]
            fixed_context = fixed_text[context_start:context_end]
            logger.info(f"Fixed stuck words: '...{context}...' -> '...{fixed_context}...'")
    
    return fixed_text

def process_thesis_data(thesis_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process and clean the thesis data using pattern-based approaches:
    1. Build a name frequency map to identify common supervisors
    2. Clean author names and extract embedded supervisors
    3. Clean supervisor lists
    4. Fix stuck words in abstracts using KeyBERT
    """
    # Build name frequency map and identify supervisors
    name_freq_map = build_name_frequency_map(thesis_data)
    known_supervisors = identify_supervisors(name_freq_map)
    
    logger.info(f"Top potential supervisors: {list(known_supervisors)[:10]}")
    
    # Initialize KeyBERT model
    logger.info("Initializing KeyBERT model...")
    try:
        kw_model = KeyBERT()
        logger.info("KeyBERT model initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing KeyBERT model: {e}")
        logger.warning("Continuing without KeyBERT, will use only regex-based cleaning")
        kw_model = None
    
    cleaned_data = []
    
    for thesis in thesis_data:
        # Create a copy to avoid modifying the original
        cleaned_thesis = thesis.copy()
        
        # Clean author name and extract any supervisors
        if 'author' in cleaned_thesis:
            original_author = cleaned_thesis['author']
            
            # Try to separate author and supervisors
            author, extracted_supervisors = separate_author_supervisor(original_author, known_supervisors)
            
            # Update the author
            if author:
                cleaned_thesis['author'] = author
                if author != original_author:
                    logger.info(f"Cleaned author: '{original_author}' -> '{author}'")
            
            # Add extracted supervisors to the existing list
            if extracted_supervisors:
                logger.info(f"Extracted supervisors from author: {extracted_supervisors}")
                current_supervisors = cleaned_thesis.get('supervisor', [])
                if isinstance(current_supervisors, str):
                    current_supervisors = [current_supervisors] if current_supervisors else []
                
                current_supervisors.extend(extracted_supervisors)
                cleaned_thesis['supervisor'] = current_supervisors
        
        # Clean supervisor list
        if 'supervisor' in cleaned_thesis and cleaned_thesis['supervisor']:
            original_supervisors = cleaned_thesis['supervisor']
            if isinstance(original_supervisors, str):
                original_supervisors = [original_supervisors]
            
            cleaned_supervisors = clean_supervisor_list(original_supervisors)
            if cleaned_supervisors != original_supervisors:
                logger.info(f"Cleaned supervisors: {original_supervisors} -> {cleaned_supervisors}")
            
            cleaned_thesis['supervisor'] = cleaned_supervisors
        
        # Fix stuck words in abstract
        if 'abstract' in cleaned_thesis and cleaned_thesis['abstract']:
            if kw_model:
                cleaned_thesis['abstract'] = fix_abstract_with_keybert(cleaned_thesis['abstract'], kw_model)
            else:
                cleaned_thesis['abstract'] = fix_sticked_words(cleaned_thesis['abstract'])
        
        cleaned_data.append(cleaned_thesis)
    
    return cleaned_data

def main():
    """Main function to process the thesis data."""
    logger.info("Starting pattern-based cleaning process for thesis data")
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return
    
    # Load data
    thesis_data = load_data(INPUT_FILE)
    if not thesis_data:
        logger.error("No data loaded. Exiting.")
        return
    
    logger.info(f"Loaded {len(thesis_data)} thesis entries")
    
    # Process the data with pattern-based approaches
    cleaned_data = process_thesis_data(thesis_data)
    
    # Save processed data
    save_data(cleaned_data, OUTPUT_FILE)
    
    logger.info("Pattern-based cleaning completed successfully")

if __name__ == "__main__":
    main()