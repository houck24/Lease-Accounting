FROM python:3.11-slim

# Install LibreOffice and font utilities
RUN apt-get update && apt-get install -y \
    libreoffice \
    fontconfig \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install SAGE custom fonts
RUN mkdir -p /usr/local/share/fonts/custom \
    && cp /app/SAGE*.TTF /usr/local/share/fonts/custom/ \
    && fc-cache -f -v

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
