# producer/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY sensors_producer.py .

RUN pip install kafka-python requests

CMD ["python", "sensors_producer.py"]