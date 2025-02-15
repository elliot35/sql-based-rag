from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database.database import get_engine
from backend.sql_agent import generate_sql_from_question, explain_query_execution
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

app = FastAPI(
    title="SQL-Based RAG Service",
    description="This API converts natural language questions into SQL queries, executes them, and explains the process.",
)

class QueryRequest(BaseModel):
    question: str
    target_db: str = "default"  # Optional: specify which database to target.

class QueryResponse(BaseModel):
    question: str
    sql_query: str
    result: str  # The query result as a string (for simplicity).
    explanation: str

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