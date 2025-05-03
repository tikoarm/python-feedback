FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/main.py ./main.py
COPY app/bot ./bot
COPY app/database ./database
COPY app/web ./web
COPY app/cache ./cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]