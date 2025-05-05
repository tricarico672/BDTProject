FROM python:3.10-slim

WORKDIR /app
COPY sensors_consumer.py .

RUN pip install fastapi uvicorn kafka-python

CMD ["uvicorn", "sensors_consumer:app", "--host", "0.0.0.0", "--port", "8002"]