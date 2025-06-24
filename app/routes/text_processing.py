from flask import Blueprint, request, jsonify
from app.services.text_processor import get_keywords
from loguru import logger

bp = Blueprint("text_processing", __name__)
route_logger = logger.bind(name="TEXT_ROUTE")

@bp.route("/text/send-text", methods=['POST'])
def send_text():
    """
    Endpoint to receive text via POST, process it and return extracted keywords.

    Returns:
        JSON: With the result or an error message.
    """
    try:
        data = request.get_json()
        if not data:
            route_logger.warning("No JSON data received")
            return jsonify({"status": "error", "message": "You must send data in JSON"}), 400

        question = data.get('text', '')
        if not question:
            route_logger.warning("No 'text' field in request")
            return jsonify({"status": "error", "message": "You must send data in field 'text'"}), 400

        result = get_keywords(question)
        route_logger.info(f"Keywords extracted: {result}")
        return jsonify({"status": "success", "message": "Text successfully received", "result": result}), 200

    except ValueError as ve:
        route_logger.error(f"Value error: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        route_logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500