from loguru import logger
from app.models import TopicModel

topic_model = TopicModel()

formatting_logger = logger.bind(name=__name__)

def format_search_results(search_results) -> list:
    """
    Format search results to display relevant information.
    """
    if not search_results:
        formatting_logger.warning("No relevant questions were found for your query.")
        return []
    
    formatted_results = []
    
    for i, result in enumerate(search_results, 1):
        formatted_result = {
            'rank': i,
            'question': result['question'],
            'project': result['project'].upper(),
            'topic': topic_model.get_topic_by_id(result['topic_id']),
            'question_id': result['question_id'],
            'score': round(result['final_score'], 2),
            'matches': result['matched_terms'],
            'match_breakdown': {
                'exact': len(result['match_details']['exact_matches']),
                'synonyms': len(result['match_details']['synonym_matches']), 
                'related': len(result['match_details']['related_matches'])
            }
        }
        formatted_results.append(formatted_result)
    
    return formatted_results