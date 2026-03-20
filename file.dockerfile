FROM python:3.11-slim

# Install system dependencies including LibreOffice and fontconfig
RUN apt-get update && apt-get install -y \
    libreoffice \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and install fonts
RUN mkdir -p /usr/local/share/fonts/custom
COPY fonts/ /usr/local/share/fonts/custom/

# Refresh font cache
RUN fc-cache -f -v

# Copy remaining application files
COPY . .

# Expose port
EXPOSE 10000

# Run the application
CMD ["python", "app.py"]
