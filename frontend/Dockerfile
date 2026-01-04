# frontend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create requirements file for frontend
RUN echo "streamlit==1.28.0" > /tmp/requirements.txt && \
    echo "requests==2.31.0" >> /tmp/requirements.txt && \
    echo "pandas==2.0.3" >> /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy frontend app
COPY streamlit_app.py .

# Create .streamlit config directory
RUN mkdir -p ~/.streamlit

# Create streamlit config
RUN echo "[client]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Run streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
