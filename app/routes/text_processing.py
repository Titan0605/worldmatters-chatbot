from flask import Blueprint, request, jsonify
from loguru import logger

from app.models import KeywordsModel
from app.services.text_processor import get_keywords
from app.services.question_score import search_relevant_questions
from app.utils.formatting import format_search_results

bp = Blueprint("text_processing", __name__)
route_logger = logger.bind(name="TEXT_ROUTE")

@bp.route("/text/send-text", methods=['POST'])
def send_text():
    """
    Endpoint to receive text via POST, process it and return extracted keywords.

    Returns:
        JSON: With the result or an error message.
    """
    kw_model = KeywordsModel()
    try:
        data = request.get_json()
        if not data:
            route_logger.warning("No JSON data received")
            return jsonify({"status": "error", "message": "You must send data in JSON"}), 400

        question = data.get('text', '')
        if not question:
            route_logger.warning("No 'text' field in request")
            return jsonify({"status": "error", "message": "You must send data in field 'text'"}), 400

        try:
            # Proccess the text and get the keywords
            result = get_keywords(question)
        except Exception as e:
            route_logger.error(f"Error extracting keywords: {e}")
            return jsonify({"status": "error", "message": "Error extracting keywords"}), 500

        try:
            # Search in DB for more words to extend the search
            result['extended_words'] = kw_model.get_extended_words(result['key_words'])
        except Exception as e:
            route_logger.error(f"Error getting extended words: {e}")
            result['extended_words'] = {}

        route_logger.info(f"Keywords extracted: {result}")

        try:
            # With all the words search between the questions to get the top 5(default)
            top_questions = search_relevant_questions(
                result['key_words'],
                result['extended_words']
            )
        except Exception as e:
            route_logger.error(f"Error searching relevant questions: {e}")
            top_questions = []

        try:
            # Format the results for a better understanding of the scores
            formatted_questions = format_search_results(top_questions)
        except Exception as e:
            route_logger.error(f"Error formatting search results: {e}")
            formatted_questions = []

        route_logger.info(f"Top questions: {formatted_questions}")

        return jsonify({"status": "success", "message": "Text successfully received", "result": result}), 200

    except ValueError as ve:
        route_logger.error(f"Value error: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        route_logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500