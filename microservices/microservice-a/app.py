from flask import Flask, request
from confluent_kafka import Producer
import socket

app = Flask(__name__)
app.debug = True  # Ensure debug mode is on to expose the full traceback

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

    if data == "trigger_error":
        # 👇 Simulate an internal coding error (e.g., calling `.encode()` on None)
        # 🛠️ Possible fix: Validate that `data` is a string before calling .encode()
        bogus = None
        bogus.encode('utf-8')  # This will raise: AttributeError: 'NoneType' object has no attribute 'encode'

    try:
        producer.produce('my-topic', value=data.encode('utf-8'))
        producer.flush()
        return 'Message sent', 200
    except Exception as e:
        return f'Error sending message: {e}', 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)