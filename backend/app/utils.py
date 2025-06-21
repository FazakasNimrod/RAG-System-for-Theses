"""
Stop words list for filtering common words from search queries.
This improves search relevance by focusing on meaningful content words.
"""

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", 
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", 
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", 
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", 
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", 
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", 
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", 
    "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", 
    "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", 
    "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

HUNGARIAN_STOP_WORDS = {
    "a", "az", "egy", "és", "vagy", "van", "volt", "hogy", "nem", "mint", "de", "ha", "kell",
    "meg", "is", "azt", "ki", "ez", "csak", "ezt", "minden", "fel", "amely", "olyan", "azok",
    "mi", "majd", "már", "még", "lehet", "mert", "itt", "között", "kell", "neki", "nélkül",
    "aki", "ami", "amely", "melyek", "össze", "át", "fog", "tud", "lesz", "tehát", "így", "úgy"
}

ROMANIAN_STOP_WORDS = {
    "a", "acea", "aceasta", "această", "aceea", "acei", "aceia", "acel", "acela", "acele", "acelea",
    "acest", "acesta", "aceste", "acestea", "aceşti", "aceştia", "acolo", "acum", "ai", "aia", "aibă",
    "am", "ar", "are", "aş", "aşa", "aţi", "au", "avea", "avem", "aveţi", "azi", "ca", "că", "căci",
    "când", "care", "cărei", "căror", "cărui", "cât", "câte", "câţi", "către", "ce", "cel", "ceva",
    "ci", "cine", "cineva", "cât", "câtva", "cu", "cum", "cumva", "da", "dă", "dacă", "dar", "dată",
    "de", "deci", "deja", "deoarece", "departe", "deşi", "din", "dintr", "dintre", "doar", "după",
    "ea", "ei", "el", "ele", "eram", "este", "eşti", "eu", "face", "fără", "fi", "fie", "fiecare",
    "fiind", "fostă", "în", "înainte", "înaintea", "încât", "încît", "încotro", "între", "întrucât",
    "întrucît", "îţi", "la", "lângă", "le", "li", "lor", "lui", "mă", "mai", "mea", "mei", "mele",
    "mereu", "meu", "mi", "mine", "mult", "multă", "mulţi", "mulţumesc", "ne", "nevoie", "nicăieri",
    "nici", "nimeni", "nimic", "nişte", "noastră", "noastre", "noi", "nostru", "noştri", "nu", "ori",
    "oricine", "oricum", "pe", "pentru", "peste", "prea", "prima", "prin", "printr", "putea", "sa",
    "să", "săi", "sale", "sau", "său", "se", "şi", "sine", "singur", "spate", "spre", "sub", "sunt",
    "suntem", "sunteţi", "ta", "tăi", "tale", "tău", "te", "ţi", "ţie", "timpul", "tine", "toată",
    "toate", "tot", "toţi", "totuşi", "tu", "un", "una", "unde", "unei", "unele", "uneori", "unor",
    "vă", "vi", "voastră", "voastre", "voi", "voştri", "vostru", "vouă", "vreme", "vreo", "vreun"
}

ALL_STOP_WORDS = STOP_WORDS.union(HUNGARIAN_STOP_WORDS).union(ROMANIAN_STOP_WORDS)

def remove_stop_words(query):
    """
    Remove stop words from a search query
    
    Args:
        query (str): The search query
        
    Returns:
        str: The query with stop words removed
    """
    if not query:
        return ""
        
    words = query.lower().split()
    
    filtered_words = [word for word in words if word not in ALL_STOP_WORDS]
    
    if not filtered_words:
        return query
        
    return " ".join(filtered_words)

def get_important_terms(query):
    """
    Extract important terms from a query by removing stop words
    
    Args:
        query (str): The search query
        
    Returns:
        list: List of important terms in the query
    """
    if not query:
        return []
        
    words = query.lower().split()
    
    important_terms = [word for word in words if word not in ALL_STOP_WORDS and len(word) > 2]
    
    return important_terms
