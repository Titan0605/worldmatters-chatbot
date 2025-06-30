from flask import Blueprint, jsonify
from loguru import logger

from app.models import HistoryModel

history_route_logger = logger.bind(name=__name__)

bp = Blueprint("history", __name__)

@bp.route('/history', methods=['GET'])
def get_history():
    history_model = HistoryModel()
    
    try:
        history = history_model.get_history()  # Debe ser una lista de dicts
        
        return jsonify({"status": "success", "history": history})
    except Exception as e:
        history_route_logger.error(f"Error fetching history: {e}")
        return jsonify({"status": "error", "history": None})
