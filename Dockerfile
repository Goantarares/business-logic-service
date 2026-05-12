FROM python:3.11-alpine

WORKDIR /app

# Instalăm dependențele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem codul sursă
COPY src/ ./src/

EXPOSE 3003

CMD ["python", "-m", "src.app"]