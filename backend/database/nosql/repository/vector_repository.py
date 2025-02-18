from typing import Optional
from backend.database.nosql.vector_search import VectorSearch
from backend.database.nosql.mock.battery_knowledge import BATTERY_KNOWLEDGE_DATA

class VectorRepository:
    _instance: Optional[VectorSearch] = None
    _initialized: bool = False
    
    @classmethod
    def get_instance(cls) -> VectorSearch:
        """Get or create VectorSearch instance."""
        if cls._instance is None:
            cls._instance = VectorSearch()
            # Initialize with data if not already initialized
            if not cls._initialized:
                cls.initialize_with_default_data()
        return cls._instance
    
    @classmethod
    def initialize(cls, documents: list) -> None:
        """Initialize vector search with documents."""
        instance = cls.get_instance()
        instance.create_index(documents)
        cls._initialized = True
    
    @classmethod
    def initialize_with_default_data(cls) -> None:
        """Initialize with default battery knowledge data."""
        documents = [knowledge.model_dump() for knowledge in BATTERY_KNOWLEDGE_DATA]
        cls.initialize(documents) 