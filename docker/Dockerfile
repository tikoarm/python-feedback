FROM python:3.10-slim

WORKDIR /app

COPY app/main.py ./main.py
COPY app/bot ./bot
COPY app/database ./database
COPY app/web ./web
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]