from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer("raw_data", bootstrap_servers="kafka:9092")
producer = KafkaProducer(bootstrap_servers="kafka:9092")

print("Stream processor started...")

for message in consumer:
    raw = message.value.decode("utf-8")
    print(f"Received: {raw}")

    processed = raw.upper()
    producer.send('processed_data', processed.encode('utf-8'))
    print(f"Processed and sent: {processed}")
