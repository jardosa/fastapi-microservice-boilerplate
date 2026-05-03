FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app:/app/services/auth_service

COPY services/auth_service/requirements.txt ./services/auth_service/requirements.txt
RUN pip install --no-cache-dir -r ./services/auth_service/requirements.txt

COPY shared ./shared
COPY services/auth_service ./services/auth_service

WORKDIR /app/services/auth_service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
