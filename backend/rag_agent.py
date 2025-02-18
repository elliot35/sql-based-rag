from typing import List
from backend.database.nosql.model.battery_knowledge import BatteryKnowledge
from backend.sql_agent import get_llm

def explain_rag_results(question: str, sql_result: str, relevant_docs: List[BatteryKnowledge]) -> str:
    """
    Generate a comprehensive explanation combining SQL results and relevant documents.
    """
    # Create context from relevant documents
    docs_context = "\n\n".join([
        f"Document: {doc.title}\n{doc.content}\nTags: {', '.join(doc.tags)}"
        for doc in relevant_docs
    ])
    
    prompt = f"""
    Question: {question}
    
    SQL Query Results:
    {sql_result}
    
    Related Knowledge:
    {docs_context}
    
    Please provide a comprehensive explanation that:
    1. Explains the SQL query results
    2. Incorporates relevant information from the knowledge base
    3. Provides additional context and insights by combining both sources
    4. Highlights any important patterns or relationships between the data
    
    Format your response in markdown.
    """
    
    llm = get_llm()
    explanation = llm.predict(prompt)
    
    return explanation 