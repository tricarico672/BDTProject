FROM python:3.10-slim

WORKDIR /app
# COPY app.py .
COPY traffic.py .
COPY .env .

RUN pip install kafka-python requests sqlalchemy psycopg2-binary python-dotenv

CMD ["python", "-u", "traffic.py"]