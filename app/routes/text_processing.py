from flask import Blueprint, request, jsonify, render_template
from loguru import logger
import random

from app.models import KeywordsModel, ResponsesModel
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
    resp_model = ResponsesModel()
    try:
        data = request.get_json()
        if not data:
            route_logger.warning("No JSON data received")
            return jsonify({"status": "error", "message": "You must send data in JSON"}), 400

        question = data.get('text', '')
        if not question:
            route_logger.warning("No 'text' field in request")
            return jsonify({"status": "error", "message": "You must send a question"}), 400

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
        
        response_data = {
            "status": "success",
            "message": "Text successfully received",
            "result": result
        }

        # Check for exact match with any question in DB
        exact_match = None
        for q in formatted_questions:
            if question.strip().lower() == q['question'].strip().lower():
                exact_match = q
                break

        if exact_match:
            try:
                responses = resp_model.get_responses(exact_match['question_id'])
                if responses:
                    chosen_response = responses[0]  # Always pick the first for exact match
                    response_data.update({
                        "ambiguous": False,
                        "response": chosen_response,
                        "question": exact_match
                    })
                else:
                    response_data["message"] = "No se encontraron respuestas para esta pregunta"
            except Exception as e:
                route_logger.error(f"Error getting responses: {e}")
                response_data["message"] = "Error al obtener la respuesta"
        # Check if we have at least two questions to compare
        elif len(formatted_questions) >= 2:
            score_diff = abs(formatted_questions[0]['score'] - formatted_questions[1]['score'])
            if score_diff < 100:
                # Case: Ambiguous question
                top_3_questions = formatted_questions[:3]
                response_data.update({
                    "ambiguous": True,
                    "message": "No estoy seguro de qué exactamente quieres saber. ¿Podrías ser más específico?",
                    "suggestions": top_3_questions
                })
            else:
                # Case: Clear winner
                top_question = formatted_questions[0]
                try:
                    # Get responses for the top question
                    responses = resp_model.get_responses(top_question['question_id'])
                    if responses:
                        chosen_response = random.choice(responses)
                        response_data.update({
                            "ambiguous": False,
                            "response": chosen_response,
                            "question": top_question
                        })
                    else:
                        response_data["message"] = "No se encontraron respuestas para esta pregunta"
                except Exception as e:
                    route_logger.error(f"Error getting responses: {e}")
                    response_data["message"] = "Error al obtener la respuesta"
        else:
            response_data["message"] = "No tengo una respuesta a tu pregunta."

        return jsonify(response_data), 200

    except ValueError as ve:
        route_logger.error(f"Value error: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        route_logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500