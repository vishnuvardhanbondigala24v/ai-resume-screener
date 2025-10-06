import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extracts keywords from job description text.
    :param text: Job description as a string
    :return: List of unique keywords
    """
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    return list(set(keywords))  # remove duplicates
