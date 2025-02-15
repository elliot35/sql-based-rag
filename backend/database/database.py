from sqlalchemy import create_engine
import os

# Mapping of database names to their connection strings.
DATABASES = {
    "default": "postgresql+psycopg2://user:password@db:5432/mydatabase"
    # To add more databases, include additional key/value pairs.
}

def get_engine(database_name: str = "default"):
    """Get SQLAlchemy engine for the specified database."""
    if database_name != "default":
        raise ValueError(f"Database '{database_name}' not configured")
    
    # Get database URL from environment variable
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Create and return the engine
    return create_engine(database_url)