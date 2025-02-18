from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BatteryKnowledge(BaseModel):
    """Model for battery knowledge documents."""
    title: str
    content: str
    category: str
    tags: List[str]
    source: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        collection_name = "battery_knowledge" 