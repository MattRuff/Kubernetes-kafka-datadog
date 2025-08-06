# 🧪 Kafka Microservices Lab (Helm + Datadog)

## 📘 Overview

This lab sets up a Kafka-based microservices application and instruments it with Datadog observability. You'll:

- Install the Datadog Agent using a prebuilt `datadog.yaml`.
- Deploy Kafka and microservices using a Helm chart.
- Monitor Kafka and services using Datadog.

## 🚀 Lab Steps

### 1. ✅ Prerequisites
- A Kubernetes cluster
- `kubectl` configured to point to your cluster
- Helm v3+
- Datadog API key


### 2. 📥 Install the Datadog Agent

```bash
helm repo add datadog https://helm.datadoghq.com
helm install datadog-operator datadog/datadog-operator
kubectl create secret generic datadog-secret --from-literal api-key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

kubectl create namespace datadog
kubectl apply -f datadog.yaml -n datadog
```

### 2. 📥 Install Application
```bash
kubectl create namespace kafka
helm install kafka-lab ./kafka-app -n kafka
```
### After installation
```bash
kubectl get pods

kubectl apply -f ./microservices/load-generate/generate.yaml

kubectl port-forward svc/microservice-b -n kafka 8080:80
```

Go to http://localhost:8080/api/messages to see messages