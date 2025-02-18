from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional

class MongoDBConnection:
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[AsyncIOMotorClient] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(
                os.getenv("MONGO_URI"),
                serverSelectionTimeoutMS=5000
            )
            self._db = self._client[os.getenv("MONGO_DB")]
    
    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client
    
    @property
    def db(self):
        return self._db
    
    def get_collection(self, collection_name: str):
        return self._db[collection_name] 