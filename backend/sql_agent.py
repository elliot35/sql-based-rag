from typing import Any, List, Optional
import os
from backend.database.sql.database import get_engine
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.llms import LlamaCpp
from langchain_openai import ChatOpenAI

def get_llm():
    """Initialize and return the configured LLM."""
    llm_provider = os.getenv("LLM_PROVIDER", "local").lower()
    
    if llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI")
        
        return ChatOpenAI(
            api_key=api_key,
            temperature=0.1,
            model="gpt-4o-mini"
        )
    
    elif llm_provider == "local":
        return LlamaCpp(
            model_path="./models/llama-2-7b-chat.gguf",
            temperature=0.1,
            max_tokens=1024,
            top_p=0.9,
            n_ctx=2048,
            n_gpu_layers=1
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")

def format_sql_query(query: str) -> str:
    """Format a SQL query with our custom markers."""
    return f"FINAL QUERY START:\n{query}\nFINAL QUERY END"

def is_valid_sql(query: str) -> bool:
    """
    Check if a string looks like a valid SQL query.
    
    Args:
        query (str): The string to check
    
    Returns:
        bool: True if the string looks like SQL, False otherwise
    """
    # List of common SQL keywords that typically start a query
    sql_starters = ['select', 'with', 'update', 'delete', 'insert']
    
    # Clean and lower-case the query
    cleaned_query = query.strip().lower()
    
    # Check if it starts with a SQL keyword
    return any(cleaned_query.startswith(keyword) for keyword in sql_starters)

def generate_sql_from_question(question: str, db_url: str) -> tuple[str, str]:
    """
    Generate SQL query from a natural language question using LLM.
    
    Args:
        question (str): The natural language question
        db_url (str): Database connection URL
    
    Returns:
        tuple[str, str]: A tuple containing (extracted_sql_query, full_llm_output)
    """
    # Initialize the LLM
    llm = get_llm()
    engine = get_engine()
    
    # Create SQLDatabase instance from the engine
    db = SQLDatabase(engine=engine)
    
    # Create the SQL toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create the SQL agent
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,  # Allow multiple attempts
    )

    # Add context to the question
    enhanced_question = f"""
    Using the database schema provided, please help me answer this question:
    {question}
    
    Please make sure to:
    1. Examine the available tables and their relationships
    2. Generate a valid SQL query that answers the question
    3. Return ONLY the SQL query starting with SELECT, INSERT, UPDATE, or DELETE
    4. Do not include any explanations, comments, or natural language responses
    5. Do not directly return the query results, only the query itself
    
    Example of a good response:
    SELECT column FROM table WHERE condition;
    
    Example of a bad response:
    The query results show that...
    Here's what I found...
    """

    # Execute the agent with the enhanced question
    try:
        result = agent_executor.run(enhanced_question)
        print(f"agent_result: {result}")
        if "I don't know" in result or not result.strip() or not is_valid_sql(result):
            raise ValueError("The LLM was unable to generate a valid SQL query. Please provide more context or rephrase the question.")
        
        # Extract the SQL query (assuming it's the entire result from the agent)
        sql_query = result.strip()
        
        # Additional validation
        if not is_valid_sql(sql_query):
            raise ValueError("Generated response is not a valid SQL query")
        
        # Format the result with our markers
        formatted_result = format_sql_query(sql_query)
        
        return sql_query, formatted_result
        
    except Exception as e:
        if "parsing errors" in str(e).lower():
            raise ValueError("Failed to generate valid SQL. Please rephrase your question or provide more context.")
        elif isinstance(e, ValueError):
            raise
        raise

def explain_query_execution(question: str, sql_query: str, result: str) -> str:
    """
    Generate a natural language explanation of the SQL query execution using ChatLlamaAPI.
    
    Args:
        question (str): Original natural language question
        sql_query (str): Generated SQL query
        result (str): Query execution result
    
    Returns:
        str: Natural language explanation
    """
    llm = get_llm()
    
    # Create a prompt that asks for an explanation
    prompt = f"""Given the following:
    Question: {question}
    SQL Query: {sql_query}
    Result: {result}
    
    Please provide a clear, concise explanation of:
    1. How the SQL query addresses the question
    2. What the results mean
    3. Any important insights from the data
    
    Explanation:"""
    
    # Get the explanation from the LLM
    response = llm.predict(prompt)
    
    return response