# Use Python 3.9
FROM python:3.9-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH="/app"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install streamlit plotly
RUN pip install --no-cache-dir streamlit plotly geopandas folium

EXPOSE 8000
EXPOSE 8501

# Default: open bash
CMD ["bash"]
