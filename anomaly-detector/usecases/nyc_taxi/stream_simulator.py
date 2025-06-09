import pandas as pd
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

df = pd.read_parquet("yellow_tripdata_2023-02.parquet")

df['trip_duration'] = (
    df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
).dt.total_seconds()

df = df[
    (df['trip_duration'] > 0) &
    (df['fare_amount'] > 0) &
    (df['trip_distance'] > 0)
]

for _, row in df.iterrows():
    msg = {
        "trip_duration": row['trip_duration'],
        "trip_distance": row['trip_distance'],
        "fare_amount": row["fare_amount"],
        "total_amount": row["total_amount"]
    }
    producer.send('nyc-taxi', msg)
    print("Sent: ", msg)
    time.sleep(1)