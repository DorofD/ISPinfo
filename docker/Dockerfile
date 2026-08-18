FROM python:3.12-slim

WORKDIR /app

COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/app/data"]

EXPOSE 5000

# Инициализация БД при первом старте + gunicorn (без debug-режима)
CMD ["sh", "-c", "python init_db.py && gunicorn -b 0.0.0.0:5000 --workers 2 app:app"]