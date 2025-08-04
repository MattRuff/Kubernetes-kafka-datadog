from flask import Flask, jsonify
from confluent_kafka import Consumer
from threading import Thread
from collections import deque
import time

app = Flask(__name__)
message_buffer = deque(maxlen=100)

def consume_kafka():
    consumer_conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'microservice-b-group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['my-topic'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        message = {
            "value": msg.value().decode('utf-8'),
            "timestamp": time.time() * 1000  # Approximate; can be refined
        }
        message_buffer.append(message)

@app.route('/api/messages')
def get_messages():
    return jsonify(list(message_buffer))

if __name__ == '__main__':
    Thread(target=consume_kafka, daemon=True).start()
    app.run(host='0.0.0.0', port=80)