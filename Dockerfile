FROM python:3.12-slim

WORKDIR /app

COPY backend/ ./backend
COPY backend/requirements.txt .  

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
