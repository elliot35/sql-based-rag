import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import os

# Get backend URL from environment variable or use default
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

# Configure the page
st.set_page_config(
    page_title="Smart Battery Storage Knowledge RAG Service",
    page_icon="⚡",
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
    st.title("⚡ Battery Storage Knowledge RAG Service")
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
        "Show me all batteries with their current charge levels",
        "Which batteries are installed by Installer Inc?",
        "What is the total energy output from all batteries today?",
        "Show me the tariff rates for each battery",
        "List all locations with their battery counts"
    ]
    
    if st.button("📋 Load Random Example"):
        import random
        st.session_state.question = random.choice(example_queries)

# Main content area
st.title("Smart Battery Storage Knowledge RAG Service")
st.markdown("Ask questions about your battery storage system in natural language.")

# Initialize session state for the question
if 'question' not in st.session_state:
    st.session_state.question = ""

# Query input
question = st.text_area(
    "Enter your question:",
    value=st.session_state.question,
    height=100,
    placeholder="e.g., 'Show me all batteries with charge levels below 50%'"
)

# Submit button with loading state
if st.button("🔍 Analyze", type="primary"):
    if not question:
        st.warning("⚠️ Please enter a question.")
    else:
        try:
            with st.spinner("🤔 Analyzing your question..."):
                # Make API request
                payload = {"question": question, "target_db": target_db}
                response = requests.post(f"{BACKEND_URL}/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display results in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📝 Generated SQL Query")
                        st.code(data.get("sql_query"), language="sql")
                    
                    with col2:
                        st.markdown("### 🔍 Query Result")
                        # Try to parse the result string into a more readable format
                        try:
                            # Attempt to convert string result to DataFrame
                            result_data = eval(data.get("result"))
                            if isinstance(result_data, (list, tuple)):
                                df = pd.DataFrame(result_data)
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.write(data.get("result"))
                        except:
                            st.write(data.get("result"))
                    
                    # Display explanation
                    st.markdown("### 📊 Analysis")
                    st.info(data.get("explanation"))
                    
                    st.markdown(f"*Query executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the backend service. Please ensure the backend is running.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

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