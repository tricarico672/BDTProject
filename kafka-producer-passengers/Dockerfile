FROM python:3.10-slim

WORKDIR /app
# COPY app.py .
COPY app.py .
COPY treemodel.pkl .
COPY treemodel_out.pkl .
COPY labelencoder.pkl .
COPY stop_times_passengers_shapes.csv .

RUN pip install pandas numpy kafka-python scikit-learn sqlalchemy psycopg2-binary

CMD ["python", "app.py"]