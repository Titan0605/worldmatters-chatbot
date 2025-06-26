from app.utils.db import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
from loguru import logger

kw_model_logger = logger.bind(name=__name__)

class KeywordsModel:
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
            self._collection = get_collection("keywords")
        return self._collection
    
    def get_related_words(self, words: list[str] | None = None) -> list[str]:
        if words is None:
            kw_model_logger.error("A word must be send as an argument")
            raise ValueError("Words list cannot be None")
        
        if not all(isinstance(word, str) for word in words):
            kw_model_logger.error("All elements in words list must be strings")
            raise TypeError("All elements in words list must be strings")
        
        db: Collection = self.collection
        
        pipeline = [
            {
                "$match": {
                    "word": {"$in": words}
                }
            },
            {
                "$project": {
                    "synonyms": 1,
                    "related": 1,
                }
            }
        ]
        
        try:
            cursor = db.aggregate(pipeline)
            results: list[str] = []
            
            for document in cursor:
                synonyms = document.get('synonyms', [])
                related = document.get('related', [])
                
                if synonyms:
                    kw_model_logger.info(f"Synonyms found: {synonyms}")
                    results.extend(synonyms)
                if related:
                    kw_model_logger.info(f"Related words found: {related}")
                    results.extend(related)
                
        except Exception as e:
            kw_model_logger.error(f"Error getting related words: {str(e)}")
            return []
            
        kw_model_logger.info(f"Related words successfully obtained: {results}")
        return list(set(results))  # Removing duplicates