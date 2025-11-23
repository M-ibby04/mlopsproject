# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files into the image
COPY . /app

# Install system dependencies (compiler etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages (NO TFF here)
RUN pip install --no-cache-dir \
    pandas \
    numpy==1.23.5 \
    matplotlib \
    scikit-learn \
    jupyter \
    openpyxl \
    tensorflow==2.13.1

# Default to bash; you’ll run scripts manually
CMD ["bash"]
