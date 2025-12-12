from kafka import KafkaConsumer, KafkaProducer
import time

consumer = KafkaConsumer(
    'raw_data',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000
)
producer = KafkaProducer(bootstrap_servers='kafka:9092')

print('Stream processor started')

try:
    while True:
        for message in consumer:
            raw = message.value.decode('utf-8')
            print(f'Received: {raw}')
            processed = raw.upper()
            producer.send('processed_data', processed.encode('utf-8'))
            producer.flush()
            print(f'Processed and sent: {processed}')
        time.sleep(1)
except KeyboardInterrupt:
    print('Stopping stream processor')
finally:
    consumer.close()
    producer.close()
