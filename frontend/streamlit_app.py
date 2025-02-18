import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import os
from typing import Dict, Any

# Get backend URL from environment variable or use default
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

# Configure the page
st.set_page_config(
    page_title="SQL-Based RAG Service",
    page_icon="🔍",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .sql-query {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.title("⚡ Knowledge RAG Service")
    st.markdown("---")
    
    # Database selection
    target_db = st.selectbox(
        "Select Database",
        ["default"],
        index=0
    )
    
    # Example queries
    st.markdown("### Example Queries")
    example_queries = [
        "Show me all batteries with their current charge levels and their full capacity",
        "Which batteries are installed by Installer Inc?",
        "What is the total energy output and input from all batteries on 2023-10-11, and how much does these cost?",
        "Show me the tariff rates for each battery and what company is the installer",
        "List all locations with their battery counts and the total energy output and input"
    ]
    
    # Initialize session states for both tabs if not exists
    if 'sql_question' not in st.session_state:
        st.session_state.sql_question = ""
    if 'rag_question' not in st.session_state:
        st.session_state.rag_question = ""
    
    if st.button("📋 Load Random Example"):
        import random
        random_query = random.choice(example_queries)
        st.session_state.sql_question = random_query
        st.session_state.rag_question = random_query

def query_backend(endpoint: str, question: str) -> Dict[Any, Any]:
    """Send a query to the backend API."""
    url = f"{BACKEND_URL}/{endpoint}"
    try:
        response = requests.post(
            url,
            json={"question": question, "target_db": target_db},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {str(e)}")
        return None

def display_sql_results(data: Dict[Any, Any]):
    """Display SQL query results."""
    if data and "sql_query" in data:
        st.markdown("### 🔍 SQL Query")
        st.code(data["sql_query"], language="sql")
        
        st.markdown("### 📊 Query Result")
        try:
            result_data = eval(data.get("result"))
            if isinstance(result_data, (list, tuple)):
                df = pd.DataFrame(result_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.write(data.get("result"))
        except:
            st.write(data.get("result"))

def display_rag_results(data: Dict[Any, Any]):
    """Display RAG results including relevant documents."""
    if not data:
        return

    # Display SQL Query and Results
    st.markdown("### 🔍 SQL Query")
    st.code(data["sql_query"], language="sql")
    
    st.markdown("### 📊 SQL Query Result")
    try:
        result_data = eval(data.get("sql_result"))
        if isinstance(result_data, (list, tuple)):
            df = pd.DataFrame(result_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.write(data.get("sql_result"))
    except:
        st.write(data.get("sql_result"))

    # Display Relevant Documents
    st.markdown("### 📚 Relevant Knowledge")
    for i, doc in enumerate(data.get("relevant_docs", []), 1):
        with st.expander(f"📄 {doc['title']} (Relevance: {doc['relevance_score']:.2f})"):
            st.markdown(f"**Category:** {doc['category']}")
            st.markdown(f"**Tags:** {', '.join(doc['tags'])}")
            st.markdown("**Content:**")
            st.markdown(doc['content'])

def main():
    # Header
    st.title("🤖 Smart Battery Storage Knowledge RAG Service")
    st.markdown("---")

    # Create tabs
    tab_sql, tab_rag = st.tabs(["SQL Query", "SQL + Knowledge Base (RAG)"])

    with tab_sql:
        # Regular SQL query interface
        question_sql = st.text_area(
            "Enter your question:",
            placeholder="e.g., Show me all batteries with their current charge levels",
            value=st.session_state.sql_question,
            key="sql_question"
        )

        if st.button("Generate SQL Query", key="sql_button"):
            if question_sql:
                with st.spinner("Generating SQL query and explanation..."):
                    data = query_backend("query", question_sql)
                    if data:
                        col1, col2 = st.columns([3, 2])
                        
                        with col1:
                            display_sql_results(data)
                        
                        with col2:
                            st.markdown("### 📝 Explanation")
                            st.markdown(data.get("explanation", ""))
            else:
                st.warning("Please enter a question first.")

    with tab_rag:
        # RAG interface
        question_rag = st.text_area(
            "Enter your question:",
            placeholder="e.g., Show me all batteries with their current charge levels",
            value=st.session_state.rag_question,
            key="rag_question"
        )

        if st.button("Generate Enhanced Response", key="rag_button"):
            if question_rag:
                with st.spinner("Generating comprehensive response..."):
                    data = query_backend("rag_query", question_rag)
                    if data:
                        col1, col2 = st.columns([3, 2])
                        
                        with col1:
                            display_rag_results(data)
                        
                        with col2:
                            st.markdown("### 📝 Combined Analysis")
                            st.markdown(data.get("combined_explanation", ""))
            else:
                st.warning("Please enter a question first.")

if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built by Elliot • Powered by LangChain and LlamaCpp</p>
    </div>
    """,
    unsafe_allow_html=True
) 