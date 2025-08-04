from kafka import KafkaConsumer

try:
    print("Starting consumer...")
    consumer = KafkaConsumer(
        'my-topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest', 
        group_id='my-group',
    )
    print("Consumer started, waiting for messages...")
    for msg in consumer:
        print(f"Received: {msg.value.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")