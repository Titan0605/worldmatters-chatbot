from typing import Literal
from loguru import logger

from app.models import QuestionsModel, KeywordsModel

question_model = QuestionsModel()
keywords_model = KeywordsModel()

question_score_logger = logger.bind(name=__name__)

def search_relevant_questions(processed_words: list, extended_words: dict, top_n: int =5) -> list:
    """
    Searches and ranks the most relevant queries in the database.
    
    Args:
        processed_words: Processed words from the user query
        extended_words: Synonyms and related words
        top_n: Number of results to return.
    
    Returns:
        list: List of queries ranked by relevancy
    """
    
    try:
        # Get all questions from the database
        all_questions = question_model.get_all_questions()
    except Exception as e:
        question_score_logger.error(f"Error fetching questions: {e}")
        return []

    scored_questions = []
    
    # Calculate score for each question
    for question_doc in all_questions:
        try:
            score_result = calculate_question_score(processed_words, extended_words, question_doc)
            
            # Only include questions with score > 0
            if score_result['final_score'] > 0:
                scored_questions.append(score_result)
        except Exception as e:
            question_score_logger.error(f"Error scoring question: {e}")
            continue

    # Sort by descending score
    scored_questions.sort(key=lambda x: x['final_score'], reverse=True)
    
    # Return top N results
    return scored_questions[:top_n]

def calculate_question_score(processed_words: list, extended_words: dict, question_doc: dict) -> dict:
    """
    Calculates the relevance score of a question based on word matches.
    
    Args:
        processed_words: List of processed words from the user's question
        extended_words: List of synonyms and related words
        question_doc: Question document from database
    
    Returns:
        dict: Information of the question with its calculated score
    """
    
    # Base scores according to chatbot prompt
    EXACT_MATCH_SCORE = 100  # Exact match with main keywords
    SYNONYM_SCORE = 60       # Matching with synonyms
    RELATED_SCORE = 30       # Matching with related words
    PROJECT_BONUS = 20       # Bonus for correct project context
    
    total_score = 0
    matched_terms = []
    match_details = {
        'exact_matches': [],
        'synonym_matches': [],
        'related_matches': []
    }
    
    # Safe extraction of extended words
    synonyms = extended_words.get('synonyms', []) if isinstance(extended_words, dict) else []
    related = extended_words.get('related', []) if isinstance(extended_words, dict) else []

    # Combine all search words
    if not synonyms and not related:
        all_search_words = set(processed_words)
    else:
        all_search_words = set(processed_words + synonyms + related)
    
    # Obtain keywords and synonyms for the question
    question_keywords = set(question_doc.get('keywords', []))
    question_synonyms = set(question_doc.get('synonyms', []))
    
    # 1. Verify exact matches with main keywords
    exact_matches = all_search_words.intersection(question_keywords)
    for match in exact_matches:
        total_score += EXACT_MATCH_SCORE
        matched_terms.append(match)
        match_details['exact_matches'].append(match)
    
    # 2. Verify matches with synonyms
    synonym_matches = all_search_words.intersection(question_synonyms)
    for match in synonym_matches:
        total_score += SYNONYM_SCORE
        matched_terms.append(match) 
        match_details['synonym_matches'].append(match)
    
    # 3. Check related words
    extended_set = set(synonyms + related) - set(processed_words)
    related_matches = extended_set.intersection(question_keywords.union(question_synonyms))
    for match in related_matches:
        total_score += RELATED_SCORE
        matched_terms.append(match)
        match_details['related_matches'].append(match)
    
    # 4. Project context bonus
    try:
        project_context = detect_project_context(processed_words, extended_words)
    except Exception as e:
        question_score_logger.error(f"Error detecting project context: {e}")
        project_context = None
    question_project = question_doc.get('project', '')
    
    if project_context and (project_context == question_project or question_project == 'both'):
        total_score += PROJECT_BONUS
    
    # 5. Apply base weight of the question
    base_weight = question_doc.get('weight', 50)
    weighted_score = total_score * (base_weight / 100)
    
    return {
        'question_id': question_doc.get('question_id'),
        'question': question_doc.get('question'),
        'project': question_doc.get('project'),
        'topic_id': question_doc.get('topic_id'),
        'difficulty': question_doc.get('difficulty'),
        'raw_score': total_score,
        'weighted_score': weighted_score,
        'final_score': weighted_score,
        'matched_terms': list(set(matched_terms)),
        'match_count': len(set(matched_terms)),
        'match_details': match_details,
        'base_weight': base_weight
    }

def detect_project_context(processed_words: list, extended_words: dict) -> None | Literal['waterflow'] | Literal['cleanlyfe']:
    """
    Detects which project the query refers to based on key terms.
    
    Returns:
        str: 'waterflow', 'cleanlyfe' or None
    """
    try:
        synonyms = extended_words.get('synonyms', []) if isinstance(extended_words, dict) else []
        related = extended_words.get('related', []) if isinstance(extended_words, dict) else []
        all_words = set(processed_words + synonyms + related)
    except Exception as e:
        question_score_logger.error(f"Error extracting words for project context: {e}")
        all_words = set(processed_words)
    waterflow_terms = []
    cleanlyfe_terms = []
    
    try:
        keywords_in_db = keywords_model.get_keywords_per_project()
    except Exception as e:
        question_score_logger.error(f"Error fetching keywords per project: {e}")
        return None

    for keyword in keywords_in_db:
        match keyword['project']:
            case "waterflow":
                waterflow_terms.append(keyword['word'])
            case "cleanlyfe":
                cleanlyfe_terms.append(keyword['word'])
            case 'both':
                waterflow_terms.append(keyword['word'])
                cleanlyfe_terms.append(keyword['word'])
            case _:
                continue

    waterflow_terms = set(waterflow_terms)
    cleanlyfe_terms = set(cleanlyfe_terms)

    waterflow_matches = len(all_words.intersection(waterflow_terms))
    cleanlyfe_matches = len(all_words.intersection(cleanlyfe_terms))

    if waterflow_matches > cleanlyfe_matches and waterflow_matches > 0:
        return 'waterflow'
    elif cleanlyfe_matches > waterflow_matches and cleanlyfe_matches > 0:
        return 'cleanlyfe'

    return None