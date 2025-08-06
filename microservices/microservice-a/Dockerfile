FROM python:3.9

ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL} 
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}

RUN apt-get update && apt-get install -y librdkafka-dev \
 && pip install flask confluent-kafka

WORKDIR /app
COPY . .

CMD ["python", "app.py"]