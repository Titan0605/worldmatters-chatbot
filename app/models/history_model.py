from datetime import datetime
from app.utils.db import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
from loguru import logger

history_model_logger = logger.bind(name=__name__)

class HistoryModel:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._collection: Optional[Collection] = None
        self.bot_response = None
        
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def collection(self) -> Collection:
        if self._collection is None:
            self._collection = get_collection("history")
        return self._collection
    
    def get_history(self) -> list:
        history = list(self.collection.find({},{"_id": 0, "question": 1, "response": 1, "topic": 1, "time": 1}))
        return history
    
    def new_log(self, user_question: dict, response: str) -> bool:
        query = {
            "question": user_question['question'],
            "response": response,
            "topic": user_question['topic'],
            "time": datetime.now()
        }
        
        try:
            self.collection.insert_one(query)
            history_model_logger.success("Log succesfully saved")
            return True
        except Exception as e:
            history_model_logger.error(f"Error inserting history log {str(e)}")
            return False