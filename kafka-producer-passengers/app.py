# Inside producer/app.py
from kafka import KafkaProducer
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from pickle import load

# Load your model and encoder (ensure files are included in Docker image)
with open("treemodel.pkl", "rb") as f:
    model = load(f)

with open("labelencoder.pkl", "rb") as f:
    le = load(f)

with open("treemodel_out.pkl", "rb") as f:
    model_out = load(f)

def create_kafka_producer():
    producer = None
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Kafka producer connected.")
        except Exception as e:
            print(f"Kafka not ready, retrying in 3 seconds... ({e})")
            time.sleep(3)
    return producer

# Use it in your main code
producer = create_kafka_producer()

app_start = datetime(2025, 1, 1, 0, 0, 0)

pred_id = 0

df = pd.read_csv('stop_times_passengers_shapes.csv')
unique_trip_ids = list(df['trip_id'].unique())

def get_passengers():
    global pred_id
    real_start = time.time()
    while True:
        # for each trip_id get stop and route
        for trip_id in unique_trip_ids:
            # get smaller dataset of unique trip
            for _, row in df[df['trip_id'] == trip_id].iterrows():
                # extract relevant information for each row wich corresponds to a stop
                shape_id = row.loc['shape_id']
                trip_idx = trip_id
                timestamp = row.loc['arrival_time']
                route = row.loc['route_short_name']
                stop = row.loc['stop_id'] 
                sequence = row.loc['stop_sequence']

                sim_time = app_start + pd.to_timedelta(timestamp)
                seconds = (sim_time - sim_time.replace(hour=0, minute=0, second=0)).total_seconds()
                data_x = pd.DataFrame({
                    'arrival_time': [seconds],
                    'stop_id': [stop],
                    'encoded_routes': [le.transform([str(route)])[0]]
                })

                passenger_in = int(model.predict(data_x)[0])
                passenger_out = int(model_out.predict(data_x)[0])

                payload = {
                    'prediction_id': pred_id,
                    'timestamp': sim_time.isoformat(),
                    # convert to str to avoid serialization issues when saved in JSON
                    'stop_id': str(stop),
                    'route': str(route),
                    'predicted_passengers_in': passenger_in,
                    'predicted_passengers_out': passenger_out,
                    'shape_id': str(shape_id),
                    'trip_id': str(trip_idx),
                    'stop_sequence': str(sequence)
                }
                print("Sending:", payload)
                producer.send('bus.passenger.predictions', value=payload)
                pred_id += 1
                time.sleep(0.1)

if __name__ == "__main__":
    get_passengers()