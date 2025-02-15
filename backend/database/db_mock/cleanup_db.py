from sqlalchemy import text
from backend.database.database import get_engine

def cleanup_database():
    engine = get_engine("default")
    with engine.begin() as connection:
        # Drop tables in correct order (respecting foreign key constraints)
        tables = [
            "telemetry",
            "tariffs",
            "battery_company",
            "batteries",
            "companies",
            "locations"
        ]
        
        for table in tables:
            try:
                connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                print(f"Dropped table: {table}")
            except Exception as e:
                print(f"Error dropping table {table}: {str(e)}")

if __name__ == "__main__":
    print("Starting database cleanup...")
    cleanup_database()
    print("Database cleanup completed successfully!") 