FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .

# Copy templates and static directories
COPY templates/ templates/
COPY static/ static/

EXPOSE 8000

CMD ["python", "main.py"]
