FROM python:3.10-slim

WORKDIR /app

# Copier les fichiers
COPY . .

# Installer avec mirror plus rapide
RUN pip install --no-cache-dir \
    --index-url https://pypi.org/simple/ \
    flask pymongo

CMD ["python", "app.py"]