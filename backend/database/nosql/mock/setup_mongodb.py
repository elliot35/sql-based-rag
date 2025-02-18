from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from backend.database.nosql.model.battery_knowledge import BatteryKnowledge
from backend.database.nosql.mock.battery_knowledge import BATTERY_KNOWLEDGE_DATA
from backend.database.nosql.repository.vector_repository import VectorRepository

async def setup_mongodb():
    """Set up MongoDB with necessary indexes and configurations."""
    # Connect with admin authentication
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]
    
    try:
        # Create collection
        await db.create_collection("battery_knowledge")
    except Exception as e:
        print(f"Collection might already exist: {e}")

    # Create text indexes
    await db.battery_knowledge.create_index([
        ("title", "text"),
        ("content", "text"),
        ("tags", "text")
    ])

    # Create regular indexes
    await db.battery_knowledge.create_index("category")
    await db.battery_knowledge.create_index("last_updated")

    # Insert mock data
    if await db.battery_knowledge.count_documents({}) == 0:
        documents = [knowledge.model_dump() for knowledge in BATTERY_KNOWLEDGE_DATA]
        await db.battery_knowledge.insert_many(documents)
        print("Mock data inserted successfully")
    else:
        print("Collection already contains data")

    # Initialize vector search
    documents = [knowledge.model_dump() for knowledge in BATTERY_KNOWLEDGE_DATA]
    VectorRepository.initialize(documents)
    print("Vector search index created successfully")

    print("MongoDB setup completed successfully!")

if __name__ == "__main__":
    asyncio.run(setup_mongodb()) 