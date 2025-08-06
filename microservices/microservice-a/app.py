# app.py
from flask import Flask, request, render_template, jsonify
from confluent_kafka import Producer
import socket
import threading
import requests
import time

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': socket.gethostname()
}
producer = Producer(conf)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produce', methods=['POST'])
def produce():
    data = request.json.get('message')
    if not data:
        return jsonify({'error': 'Missing message'}), 400

    if data == "trigger_error":
        # Simulated internal Python bug
        bogus = None
        bogus.encode('utf-8')  # raises AttributeError

    try:
        producer.produce('my-topic', value=data.encode('utf-8'))
        producer.flush()
        return jsonify({'status': 'Message sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-load', methods=['POST'])
def generate_load():
    def spam_kafka():
        for i in range(100):
            try:
                producer.produce('my-topic', value=f"load-message-{i}".encode('utf-8'))
            except Exception as e:
                print(f"Error sending load message: {e}")
        producer.flush()

    thread = threading.Thread(target=spam_kafka)
    thread.start()
    return jsonify({'status': 'Load generation started'})

@app.route('/messages', methods=['GET'])
def fetch_messages():
    try:
        res = requests.get("http://microservice-b/api/messages")
        messages = res.json()
        now = time.time() * 1000
        for msg in messages:
            msg['latency_ms'] = round(now - msg['timestamp'], 2)
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)