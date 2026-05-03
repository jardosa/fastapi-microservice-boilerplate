FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app:/app/services/user_service

COPY services/user_service/requirements.txt ./services/user_service/requirements.txt
RUN pip install --no-cache-dir -r ./services/user_service/requirements.txt

COPY shared ./shared
COPY services/user_service ./services/user_service

WORKDIR /app/services/user_service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
