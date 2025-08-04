from flask import Flask, request
from confluent_kafka import Producer
import socket

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': socket.gethostname()
}
producer = Producer(conf)

@app.route('/produce', methods=['POST'])
def produce():
    data = request.json.get('message')
    if not data:
        return 'Missing message', 400

    try:
        producer.produce('my-topic', value=data.encode('utf-8'))
        producer.flush()
        return 'Message sent', 200
    except Exception as e:
        return f'Error sending message: {e}', 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)