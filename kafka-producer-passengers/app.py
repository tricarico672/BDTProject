# Inside producer/app.py
from kafka import KafkaProducer
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from multiprocessing import Process
from pickle import load

# Load model and encoder 
with open("treemodel.pkl", "rb") as f:
    model = load(f)

with open("labelencoder.pkl", "rb") as f:
    le = load(f)

def create_kafka_producer():
    producer = None
    # implements retry logic until the producer is connected to the Kafka cluster
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                max_in_flight_requests_per_connection=5,  # Default is 5, reducing this can help reduce load
                batch_size=16384,
                linger_ms=100,
                acks='all'
            )
            print("Kafka producer connected.")
        except Exception as e:
            print(f"Kafka not ready, retrying in 3 seconds... ({e})")
            time.sleep(3)
    return producer

TIME_MULTIPLIER = 100
real_start = time.time()
app_start = datetime(2025, 1, 1, 6, 0, 0)

def get_simulated_time():
    elapsed_real = time.time() - real_start
    elapsed_simulated = timedelta(seconds=elapsed_real * TIME_MULTIPLIER)
    return app_start + elapsed_simulated


def get_passengers(time, stop, route):
    # this makes sure that each simulation has its own kafka producer
    producer = create_kafka_producer()
    while True:
        # sim_time = get_simulated_time()
        # seconds = (sim_time - sim_time.replace(hour=0, minute=0, second=0)).total_seconds()
        seconds = time
        data_x = pd.DataFrame({
            'arrival_time': [seconds],
            'stop_id': [stop],
            'encoded_routes': [le.transform([route])[0]]
        })

        hour_stop = 2 # the time when bus stops service
        hour_start = 6 # the time when bus starts service

        if seconds > 3600 * hour_stop and seconds < 3600 * hour_start:
            passenger_num = 0
        else:
            passenger_num = int(model.predict(data_x)[0])

        payload = {
            'timestamp': time / 3600, # sim_time.isoformat(),
            'stop_id': stop,
            'route': route,
            'predicted_passengers': passenger_num
        }
        print("Sending:", payload)
        producer.send('bus.passenger.predictions', value=payload)
        time.sleep(15)
        
with open("route_to_stops.json", "r") as f:
    route_stop_map = json.load(f)

# use multi process to generate in parallel for each stop and route
# def start_simulations():
#     processes = []
#     for route in route_stop_map:
#         for stop, time in zip(route_stop_map[route]["stops"], route_stop_map[route]["departure_times_seconds"][:len(route_stop_map[route]["stops"])]):
#             p = Process(target=get_passengers, args=(time, stop, route))
#             p.start()
#             processes.append(p)

#     for p in processes:
#         p.join()

def start_simulations():
    processes = []
    for time in range(0,100000,500):
        p = Process(target=get_passengers, args = (time, 1234, '5'))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

start_simulations()