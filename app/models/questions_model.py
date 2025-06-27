from app.utils.db import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
from loguru import logger

questions_model_logger = logger.bind(name=__name__)

class QuestionsModel:
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
            self._collection = get_collection("questions")
        return self._collection
    
    def get_all_questions(self) -> list:
        db: Collection = self.collection
        
        questions = list(db.find({}))
        
        return questions