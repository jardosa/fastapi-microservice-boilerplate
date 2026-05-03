FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app:/app/services/notification_service

COPY services/notification_service/requirements.txt ./services/notification_service/requirements.txt
RUN pip install --no-cache-dir -r ./services/notification_service/requirements.txt

COPY shared ./shared
COPY services/notification_service ./services/notification_service

WORKDIR /app/services/notification_service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
