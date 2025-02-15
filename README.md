# SQL-Based RAG Service

## Overview

A powerful SQL-based Retrieval Augmented Generation (RAG) service that bridges natural language and database queries. This service enables users to interact with databases using natural language, automatically generating and executing SQL queries while providing clear explanations of the results.

## Demo

Here's a quick walkthrough of how the service works:

![Demo Screenshot 1](assets/screenshots/result1.png)
![Demo Screenshot 2](assets/screenshots/result2.png)

1. **Natural Language Input**: Users can ask questions in plain English about their battery storage system. In this example, we ask "List all locations with their battery counts"

2. **Generated SQL Query**: 
    The service automatically generates the appropriate SQL query:
    ```sql
    SELECT l.name AS location_name, COUNT(b.id) AS battery_count 
    FROM locations l
    LEFT JOIN batteries b ON l.id = b.location_id
    GROUP BY l.id
    ORDER BY l.name;
    ```

3. **Query Results**:
    The results are displayed in a clear tabular format:
    | Location | Battery Count |
    |----------|--------------|
    | Site 1   | 2            |
    | Site 2   | 1            |

4. **Intelligent Analysis**:
    The service provides a detailed explanation of:
    - How the SQL query addresses the question
    - The query construction process:
      - Selecting location names and counting batteries
      - Using LEFT JOIN to include all locations
      - Grouping results by location ID
    - Clear interpretation of the results

## Features & Capabilities

- Receives natural language queries.
- Converts them to SQL queries using LangChain and a Llama model.
- Executes the SQL query against one or more PostgreSQL databases (using SQLAlchemy).
- Uses Llama to explain how the query was generated and what the result indicates.
- Exposes the functionality via a FastAPI API (with auto-generated Swagger documentation).
- Includes a simple Streamlit frontend for user interaction.
- Supports both OpenAI and local LLama models
- Provides detailed explanations of query results
- Handles complex database relationships and queries
- Built with scalability and extensibility in mind

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher (for local development)
- PostgreSQL 13 or higher
- 8GB+ RAM (16GB+ recommended for local LLama model)
- NVIDIA GPU (optional, for local LLama model)

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sql-based-rag.git
cd sql-based-rag
```

2. Create a .env file in the root directory:
```env
# LLM Configuration
LLM_PROVIDER=openai  # or local
OPENAI_API_KEY=your-key-here  # Required if using OpenAI

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydatabase
```

## Project Structure
```
sql-based-rag/
├── backend/                 # Backend service
│   ├── database/           # Database related code
│   │   ├── db_mock/       # Mock data generation
│   │   └── db_model/      # Database models
│   ├── Dockerfile         # Backend container definition
│   └── main.py           # FastAPI application
├── frontend/              # Streamlit frontend
├── models/               # Local LLama model storage
└── docker-compose.yml    # Service orchestration
```

## Scripts

- `start.sh`: Starts all services using Docker Compose
- `end.sh`: Stops all services and cleans up containers
- `reset_db.sh`: Resets the database with fresh mock data
- `cleanup_db.sh`: Cleans up existing database tables
- `download_model.sh`: Downloads the LLama model (for local LLM)

## Running Locally

1. Start the services:
```bash
./start.sh
```

2. Reset the database with mock data:
```bash
./reset_db.sh
```

3. Access the services:
- Frontend: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## LLM Options

### 1. OpenAI (Default)
- Requires an OpenAI API key
- Set in .env: `LLM_PROVIDER=openai`
- Better accuracy but requires API costs

### 2. Local LLama
- Runs completely locally
- Set in .env: `LLM_PROVIDER=local`
- Requires more RAM and benefits from GPU
- Download model: `./download_model.sh`

To switch between providers:
1. Update LLM_PROVIDER in .env
2. Restart services: `./end.sh && ./start.sh`

## API Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "How many batteries are in each location?",
        "target_db": "default"
    }
)

print(response.json())
```

## Roadmap

1. Query Generation Improvements
   - Enhanced accuracy in SQL generation
   - Better handling of complex queries
   - Support for more SQL operations

2. Multi-Database Support
   - Connection to multiple databases
   - Cross-database queries
   - Dynamic database switching

3. Cloud Deployment
   - AWS deployment templates
   - Azure and GCP support
   - Kubernetes configurations

4. Language Support
   - Python package
   - Node.js package
   - Support for other backend languages
   - Language-specific SDKs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 