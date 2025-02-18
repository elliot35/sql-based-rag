from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from backend.database.sql.database import get_engine
from backend.sql_agent import generate_sql_from_question, explain_query_execution
from backend.rag_agent import explain_rag_results
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import os
from typing import List
from backend.database.nosql.repository.vector_repository import VectorRepository
from backend.database.nosql.mock.battery_knowledge import BATTERY_KNOWLEDGE_DATA

app = FastAPI(
    title="SQL-Based RAG Service",
    description="This API converts natural language questions into SQL queries, executes them, and explains the process.",
)

@app.on_event("startup")
def startup_event():
    """Initialize services on startup."""
    # Initialize vector search
    documents = [knowledge.model_dump() for knowledge in BATTERY_KNOWLEDGE_DATA]
    VectorRepository.initialize(documents)
    print("Vector search initialized on startup")

# MongoDB connection
mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("MONGO_DB")]

class QueryRequest(BaseModel):
    question: str
    target_db: str = "default"  # Optional: specify which database to target.

class QueryResponse(BaseModel):
    question: str
    sql_query: str
    result: str  # The query result as a string (for simplicity).
    explanation: str

class RelevantDocument(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
    relevance_score: float

class RAGResponse(BaseModel):
    question: str
    sql_query: str
    sql_result: str
    relevant_docs: List[RelevantDocument]
    combined_explanation: str

@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    # Retrieve the SQLAlchemy engine for the given database.
    try:
        engine = get_engine(request.target_db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    # Use the engine's URL (wrapped as a string) for the SQL agent.
    db_url = str(engine.url)

    # Generate the SQL query using LangChain's SQL agent.
    try:
        sql_query, llm_output = generate_sql_from_question(request.question, db_url)
    except Exception as e:
        if isinstance(e, ValueError):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error generating SQL: {str(e)}\nPlease try rephrasing your question."
        )
    
    # Execute the generated SQL query using SQLAlchemy.
    try:
        with engine.connect() as connection:
            result_proxy = connection.execute(text(sql_query))
            # Fetch all results (for demonstration, convert to a string).
            results = result_proxy.fetchall()
            result_str = str(results)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL: {str(e)}; Query: {sql_query}")
    
    # Use the Llama model to generate an explanation.
    try:
        explanation = explain_query_execution(request.question, llm_output, result_str)
    except Exception as e:
        explanation = f"Failed to generate explanation: {str(e)}"

    return QueryResponse(
        question=request.question,
        sql_query=sql_query,
        result=result_str,
        explanation=explanation,
    )

@app.post("/rag_query", response_model=RAGResponse)
async def process_rag_query(request: QueryRequest):
    """
    Process a question using both SQL and document retrieval (RAG).
    1. Execute SQL query on structured data
    2. Retrieve relevant documents from MongoDB
    3. Combine results with an explanation
    """
    # First, process SQL query (reuse existing logic)
    sql_response = process_query(request)

    # Then, search for relevant documents using vector similarity
    try:
        # Use vector search
        vector_search = VectorRepository.get_instance()
        results = vector_search.search(request.question, k=3)

        relevant_docs = [
            RelevantDocument(
                title=doc["title"],
                content=doc["content"],
                category=doc["category"],
                tags=doc["tags"],
                relevance_score=doc["relevance_score"]
            )
            for doc in results
        ]

        # Generate combined explanation using both SQL results and relevant docs
        combined_explanation = explain_rag_results(
            question=request.question,
            sql_result=sql_response.result,
            relevant_docs=relevant_docs
        )

        return RAGResponse(
            question=request.question,
            sql_query=sql_response.sql_query,
            sql_result=sql_response.result,
            relevant_docs=relevant_docs,
            combined_explanation=combined_explanation
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving relevant documents: {str(e)}"
        ) 