import re
import unicodedata
import nltk
import spacy

from nltk.corpus import stopwords
from collections import Counter
from loguru import logger

text_logger = logger.bind(name=__name__)

try:
    # Descargar stopwords solo si no están presentes
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nlp = spacy.load("es_core_news_sm")
except Exception as e:
    text_logger.error(f"Error loading spaCy model: {e}")
    raise ImportError("The spaCy ‘es_core_news_sm’ model is not installed.")

try:
    STOPWORDS = set(stopwords.words("spanish"))
except Exception as e:
    text_logger.error(f"Error loading NLTK stopwords: {e}")
    STOPWORDS = set()

def get_keywords(texto):
    """
    Extracts keywords (nouns, verbs, adjectives) from a Spanish text, eliminating stopwords and normalizing the text.
    It uses spaCy for morphological analysis and NLTK for stopwords.

    Args:
        text (str): Input text to process.

    Returns:
        dict: Dictionary with the unique keywords and the count of each one.
            {
                "key_words": list[str],
                "count": dict[str, int]
            }
    Raises:
        ValueError: If the text is invalid or an error occurs during processing.
    """
    text_logger.info("Processing text...")
    try:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("Input text must be a non-empty string.")

        texto = texto.lower()
        texto = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")
        texto = re.sub(r"[^a-zA-Z0-9\s]", "", texto)

        doc = nlp(texto)
        key_words = []
        for token in doc:
            if token.is_alpha and token.lemma_ not in STOPWORDS and token.pos_ in ['NOUN', 'VERB', 'ADJ']:
                key_words.append(token.lemma_)
                key_words.append(token.text)
                
        key_words = list(set(key_words))
        count = Counter(key_words)
        text_logger.info('Text successfully processed')
        return {
            "key_words": key_words,
            "count": dict(count),
        }
    except Exception as e:
        text_logger.error(f"Error processing text: {e}")
        raise ValueError(f"Error processing text: {e}")
