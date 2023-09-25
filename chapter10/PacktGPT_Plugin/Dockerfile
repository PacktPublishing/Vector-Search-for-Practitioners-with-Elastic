FROM python:3.8-slim

WORKDIR /app

COPY app.py /app/app.py
COPY logo.png /app/logo.png
COPY .well-known /app/.well-known
COPY openapi.yaml /app/openapi.yaml

RUN pip install --no-cache-dir \
    quart \
    quart-cors \
    openai \
    elasticsearch \
    requests

EXPOSE 5001

ENTRYPOINT ["python", "/app/app.py"]
