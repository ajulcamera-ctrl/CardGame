FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user to reduce container escape risk
RUN useradd -m botuser
USER botuser

CMD ["python", "main.py"]
