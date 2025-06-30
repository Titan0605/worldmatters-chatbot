from app.utils.db import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
from loguru import logger

topic_model_logger = logger.bind(name=__name__)

class TopicModel:
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
            self._collection = get_collection("topics")
        return self._collection
    
    def get_topic_by_id(self, id):
        try:
            topic: dict | None = self.collection.find_one({"topic_id": f"{id}"}, {"_id": 0, "name": 1})
            
            if topic is None:
                return topic_model_logger.warning("Topic not finded")
        
            topic_model_logger.success("Topic succesfully obtained")
            return topic['name']
        except Exception as e:
            topic_model_logger.error("Error obtaining topic")