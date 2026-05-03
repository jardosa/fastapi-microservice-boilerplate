FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app:/app/services/comment_service

COPY services/comment_service/requirements.txt ./services/comment_service/requirements.txt
RUN pip install --no-cache-dir -r ./services/comment_service/requirements.txt

COPY shared ./shared
COPY services/comment_service ./services/comment_service

WORKDIR /app/services/comment_service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
