# AquaEye: Shrimp Detection, Underwater Enhancement & Spatial Clustering Pipeline
# Base image with Ubuntu 22.04 and Python 3.10
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install core system dependencies, graphics libraries for OpenCV, and Python 3
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Symlink python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create working directory
WORKDIR /app/aquaeye_project

# Copy dependency requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and data folders into container
COPY . .

# Create output directories if they don't exist
RUN mkdir -p data/raw_videos data/processed_videos data/metadata models

# Expose default port for JupyterLab (if running EDA notebook in container)
EXPOSE 8888

# Set default execution command
CMD ["python", "-m", "src.main"]
