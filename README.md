# StreamPulse

**StreamPulse** is an open-source, fault-tolerant streaming analytics platform delivering exactly-once event processing, windowed aggregations, and real-time anomaly detection at massive scale. Built on **Kafka**, **Apache Flink**, and **Kubernetes**, it empowers organizations to gain millisecond insights from high-velocity data streams.

---

## 🔖 Table of Contents

1. [✨ Features](#✨-features)
2. [🏗️ Architecture](#🏗️-architecture)
3. [🚀 Quick Start](#🚀-quick-start)

   * [Prerequisites](#prerequisites)
   * [Installation](#installation)
   * [Configuration](#configuration)
   * [Running Locally](#running-locally)
4. [⚙️ Usage](#⚙️-usage)
5. [🛣️ Roadmap](#🛣️-roadmap)
6. [🤝 Contributing](#🤝-contributing)
7. [⚖️ License](#⚖️-license)
8. [📬 Contact](#📬-contact)

---

## ✨ Features

* **Exactly-Once Processing**: Leveraging Flink checkpointing and savepoints for zero data loss or duplication.
* **Windowed Aggregations**: Tumbling, sliding, and session windows with late-arrival handling.
* **Anomaly Detection**: Built-in z-score and EWMA algorithms for real-time alerting.
* **Scalable Ingestion**: Partitioned Kafka topics for high-throughput event ingestion.
* **Time-Series Storage**: Optimized Cassandra schema for fast writes and time-range queries.
* **Low-Latency API**: REST and WebSocket endpoints for real-time metric retrieval and alerts.
* **Observability**: Integrated with Prometheus, Grafana, and Jaeger for full-system monitoring and tracing.

---

## 🏗️ Architecture

1. **Producers**: Python/Go clients emit JSON events to Kafka.
2. **Kafka**: Durable, partitioned event log ensuring ordering and throughput.
3. **Flink Jobs**: Stateful stream processing with event-time semantics, watermarking, and anomaly logic.
4. **Cassandra**: Time-series datastore keyed by `(metric_id, window_start)`.
5. **API Layer**: FastAPI (Python) or Go server exposing metrics and raw data.
6. **Observability Stack**: Prometheus for metrics, Grafana dashboards, Jaeger for tracing.

---

## 🚀 Quick Start

### Prerequisites

* Docker & Docker Compose **or** Kubernetes (Minikube/GKE)
* Helm 3 & kubectl
* Java 8+ (for Flink jobs)
* Python 3.8+ (producer scripts)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/ankandas/stream-pulse.git
cd stream-pulse

# 2. Deploy services via Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install kafka bitnami/kafka --namespace stream-pulse --create-namespace
helm install cassandra bitnami/cassandra --namespace stream-pulse
helm install prometheus prometheus-community/kube-prometheus-stack --namespace stream-pulse
helm install grafana grafana/grafana --namespace stream-pulse
helm install flink bitnami/flink --namespace stream-pulse
```

### Configuration

Edit `config/application.yaml` to set your Kafka brokers, Cassandra contact points, and API ports.

### Running Locally

Use Docker Compose for quick local deployment:

```bash
docker-compose up -d
```

Start the API server:

```bash
cd api
./gradlew bootRun   # or `go run main.go` for Go implementation
```

---

## ⚙️ Usage

1. **Start producers** (synthetic or public dataset):

   ```bash
   python producers/send_events.py --rate 1000
   ```
2. **Submit Flink job**:

   ```bash
   flink run -c com.streampulse.jobs.StreamJob jobs/stream-pulse.jar
   ```
3. **Retrieve metrics**:

   ```bash
   curl "http://localhost:8080/metrics?start=<ISO8601>&end=<ISO8601>"
   ```

---

## 🛣️ Roadmap

*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and pull request process.

---

## ⚖️ License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## 📬 Contact

Created by **Ankan Das** – follow me on Twitter: [@ankandas99](https://x.com/ankandas99)
Email: [dasankan84@gmail.com](mailto:dasankan84@gmail.com)

---
