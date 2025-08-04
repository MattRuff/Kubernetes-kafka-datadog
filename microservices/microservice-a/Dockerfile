FROM python:3.9

RUN apt-get update && apt-get install -y librdkafka-dev \
 && pip install flask confluent-kafka

WORKDIR /app
COPY . .

CMD ["python", "app.py"]