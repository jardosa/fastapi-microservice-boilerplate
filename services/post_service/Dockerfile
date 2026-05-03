FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app:/app/services/post_service

COPY services/post_service/requirements.txt ./services/post_service/requirements.txt
RUN pip install --no-cache-dir -r ./services/post_service/requirements.txt

COPY shared ./shared
COPY services/post_service ./services/post_service

WORKDIR /app/services/post_service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
