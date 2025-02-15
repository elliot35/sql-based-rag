FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend code
COPY frontend/streamlit_app.py .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"] 