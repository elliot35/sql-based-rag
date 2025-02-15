FROM python:3.9-slim

# Install build-essential, cmake, and git
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create models directory
RUN mkdir -p models

# Download script for the model
COPY backend/scripts/download_model.sh .
RUN chmod +x download_model.sh

# Copy the backend requirements file and install packages
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the backend code
COPY backend/ backend/

# Make the entry point script executable
COPY backend/scripts/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set the entry point
ENTRYPOINT ["./entrypoint.sh"]

# Default command (can be overridden)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 