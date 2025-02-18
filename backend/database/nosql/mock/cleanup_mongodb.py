from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from backend.database.nosql.model.battery_knowledge import BatteryKnowledge

async def cleanup_mongodb():
    """Clean up all collections in MongoDB."""
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]
    
    # Get the collection
    collection = db[BatteryKnowledge.Config.collection_name]
    
    try:
        # Drop the entire collection (this removes indexes too)
        await collection.drop()
        print(f"Collection {BatteryKnowledge.Config.collection_name} dropped successfully")
    except Exception as e:
        print(f"Warning: Could not drop collection: {str(e)}")

    try:
        # Recreate the collection
        await db.create_collection(BatteryKnowledge.Config.collection_name)
        print(f"Collection {BatteryKnowledge.Config.collection_name} recreated")
    except Exception as e:
        print(f"Warning: Could not recreate collection: {str(e)}")
    
    print("MongoDB cleanup completed successfully")

if __name__ == "__main__":
    asyncio.run(cleanup_mongodb()) 