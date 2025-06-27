from app.utils.db import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional, List, Dict, Any
from loguru import logger

responses_logger = logger.bind(name=__name__)

class ResponsesModel:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._collection: Optional[Collection] = None
        
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def collection(self) -> Collection:
        if self._collection is None:
            self._collection = get_collection("responses")
        return self._collection
    
    def get_responses(self, question_id: str) -> List[Dict[str, Any]]:
        """Get all responses for a given question ID.

        Args:
            question_id (str): The ID of the question

        Returns:
            List[Dict[str, Any]]: List of response objects
        """
        try:
            responses = list(self.collection.find({"question_id": question_id}, {"_id": 0, "response_text": 1}))
            return responses
        except Exception as e:
            responses_logger.error(f"Error getting responses: {e}")
            return []