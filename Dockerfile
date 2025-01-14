
# Dockerfile
FROM python:3.9-slim

# Install system dependencies for Selenium
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libx11-xcb1 \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and display
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set PYTHONPATH so `pages` and `steps` modules are available
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy project files into the Docker container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run either API or UI tests based on TEST_TYPE
CMD ["sh", "-c", "pytest ${TEST_TYPE:-tests} --cucumberjson=reports/report.json --html=reports/report.html --self-contained-html"]


