# Real-Time E-commerce Event Pipeline

*A beginner-friendly, end-to-end streaming data pipeline using Aiven Kafka, PostgreSQL, and Grafana for real-time analytics.*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Kafka](https://img.shields.io/badge/kafka-streaming-orange.svg)](https://kafka.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-database-blue.svg)](https://www.postgresql.org/)
[![Grafana](https://img.shields.io/badge/grafana-visualization-orange.svg)](https://grafana.com/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Grafana Setup](#grafana-setup)
- [Sample Queries](#sample-queries)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [Contributing](#contributing)

---

## Overview

This project demonstrates a complete real-time data pipeline that simulates an e-commerce order processing system. Perfect for learning streaming architectures and real-time analytics.

### What You'll Build

A lightweight event-driven system that:

1. **Generates** realistic fake order events using Python & Faker
2. **Streams** events through Aiven Kafka for real-time processing
3. **Consumes** and persists data in Aiven PostgreSQL
4. **Visualizes** live metrics and KPIs in Grafana dashboards

### Key Learning Outcomes

- Understanding event-driven architectures
- Working with Apache Kafka for stream processing
- Real-time data persistence strategies
- Building live analytics dashboards
- Managing SSL certificates and secure connections

---

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────────┐    ┌─────────────┐
│   Python    │───▶│ Aiven Kafka  │───▶│ Python Consumer │───▶│ Aiven PostgreSQL│───▶│   Grafana   │
│  Producer   │    │   (Topic:    │    │   (Group: orders)│    │  (Table: order_ │    │ Dashboards  │
│  (Faker)    │    │order_events) │    │                 │    │     events)     │    │             │
└─────────────┘    └──────────────┘    └─────────────────┘    └────────────────┘    └─────────────┘
```

**Data Flow:**
1. Producer generates order events every 1-5 seconds
2. Events published to Kafka topic `order_events`
3. Consumer reads from topic and validates data
4. Valid events inserted into PostgreSQL
5. Grafana queries PostgreSQL for live visualizations

---

## Prerequisites

### Required Services
- **Aiven Account** (free tier available)
- **Grafana Cloud Account** or local Grafana instance
- **Python 3.8+** installed locally

### Aiven Services to Create
1. **Kafka Service**
   - Enable REST API access
   - Enable public access
   - Download SSL certificates
2. **PostgreSQL Service**
   - Enable public access
   - Note connection URI

---

## Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd real_time_pipeline
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Download SSL Certificates
From your Aiven Kafka service dashboard:
- Download `ca.pem`
- Download `service.cert` 
- Download `service.key`
- Place all three files in the project root directory

### 4. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` with your Aiven service details:
```env
KAFKA_BOOTSTRAP=your-kafka-service-uri.aivencloud.com:17971
PG_URI=postgres://avnadmin:password@pg-xxxxx.g.aivencloud.com:17972/defaultdb?sslmode=require
```

### 5. Set Up Kafka Topic
In Aiven Console:
- Navigate to your Kafka service
- Go to **Topics** → **Create Topic**
- Name: `order_events`
- Partitions: 1 (sufficient for demo)
- Replication: 2 (default)

### 6. Set Up PostgreSQL Table
Connect to your PostgreSQL instance and run:
```sql
CREATE TABLE order_events (
    id SERIAL PRIMARY KEY,
    order_id TEXT NOT NULL,
    customer TEXT NOT NULL,
    amount FLOAT NOT NULL,
    product TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Add indexes for better query performance
CREATE INDEX idx_order_events_timestamp ON order_events(timestamp);
CREATE INDEX idx_order_events_customer ON order_events(customer);
```

### 7. Run the Pipeline
Open two terminal windows:

**Terminal 1 - Producer:**
```bash
python producer.py
```

**Terminal 2 - Consumer:**
```bash
python consumer.py
```

You should see output like:
```
Producer: Sent order {'order_id': 'ORD-1234', 'customer': 'Alice Johnson', 'amount': 89.99}
Consumer: Inserted order ORD-1234 for Alice Johnson ($89.99)
```

---

## Project Structure

```
real_time_pipeline/
├── producer.py              # Event generator (Kafka producer)
├── consumer.py              # Event processor (Kafka consumer)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── README.md               # This file
├── ca.pem                  # Kafka SSL certificate authority
├── service.cert            # Kafka SSL certificate
├── service.key             # Kafka SSL private key
├── grafana/
│   ├── dashboard.json      # Pre-built dashboard
│   └── datasource.yaml     # PostgreSQL data source config
├── scripts/
│   ├── setup_db.sql        # Database initialization
│   └── test_connection.py  # Connection testing utility
└── docs/
    ├── SETUP.md            # Detailed setup guide
    └── TROUBLESHOOTING.md  # Common issues and fixes
```

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KAFKA_BOOTSTRAP` | Kafka broker endpoint | `kafka-xxx.aivencloud.com:17971` |
| `PG_URI` | PostgreSQL connection string | `postgres://user:pass@host:port/db` |
| `LOG_LEVEL` | Logging verbosity | `INFO` (DEBUG, WARNING, ERROR) |
| `PRODUCER_INTERVAL` | Seconds between events | `2` |
| `BATCH_SIZE` | Consumer batch size | `100` |

### SSL Certificate Setup

Ensure these files are present in the project root:
- `ca.pem` - Certificate Authority
- `service.cert` - Client certificate  
- `service.key` - Client private key

**File permissions should be restricted:**
```bash
chmod 600 service.key
chmod 644 service.cert ca.pem
```

---

## Running the Pipeline

### Development Mode
```bash
# Terminal 1: Start producer (generates 1 event every 2 seconds)
python producer.py

# Terminal 2: Start consumer (processes events in real-time)
python consumer.py
```

### Production Considerations
```bash
# Run with higher event frequency
PRODUCER_INTERVAL=0.5 python producer.py

# Run consumer with larger batch size
BATCH_SIZE=500 python consumer.py

# Background execution
nohup python producer.py > producer.log 2>&1 &
nohup python consumer.py > consumer.log 2>&1 &
```

---

## Grafana Setup

### 1. Add PostgreSQL Data Source
1. Open Grafana → **Configuration** → **Data Sources**
2. Click **Add data source** → **PostgreSQL**
3. Configure connection:
   ```
   Host: pg-xxxxx.g.aivencloud.com:17972
   Database: defaultdb
   User: avnadmin
   Password: [your-password]
   SSL Mode: require
   ```
4. Click **Save & Test**

### 2. Import Dashboard
1. Go to **Dashboards** → **Import**
2. Upload `grafana/dashboard.json`
3. Select your PostgreSQL data source
4. Click **Import**

### 3. Custom Dashboard Panels

Create these visualizations:

**Orders Per Minute (Time Series)**
```sql
SELECT 
  date_trunc('minute', timestamp) as time,
  count(*) as orders
FROM order_events 
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY time 
ORDER BY time;
```

**Revenue Over Time (Time Series)**
```sql
SELECT 
  date_trunc('hour', timestamp) as time,
  sum(amount) as revenue
FROM order_events 
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY time 
ORDER BY time;
```

**Top Customers (Table)**
```sql
SELECT 
  customer,
  count(*) as orders,
  sum(amount) as total_spent,
  avg(amount) as avg_order
FROM order_events 
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY customer 
ORDER BY total_spent DESC 
LIMIT 10;
```

---

## Sample Queries

### Analytics Queries

| Metric | SQL Query |
|--------|-----------|
| **Orders per minute** | `SELECT date_trunc('minute', timestamp) AS t, COUNT(*) FROM order_events WHERE timestamp > NOW() - INTERVAL '1 hour' GROUP BY t ORDER BY t` |
| **Hourly revenue** | `SELECT date_trunc('hour', timestamp) AS h, SUM(amount) FROM order_events WHERE timestamp > NOW() - INTERVAL '24 hours' GROUP BY h ORDER BY h` |
| **Top customers** | `SELECT customer, COUNT(*) as orders, SUM(amount) AS total FROM order_events GROUP BY customer ORDER BY total DESC LIMIT 10` |
| **Average order value** | `SELECT date_trunc('hour', timestamp) AS h, AVG(amount) FROM order_events GROUP BY h ORDER BY h` |
| **Daily totals** | `SELECT DATE(timestamp) as day, COUNT(*) as orders, SUM(amount) as revenue FROM order_events GROUP BY day ORDER BY day DESC` |

### Monitoring Queries

```sql
-- Check data freshness
SELECT MAX(timestamp) as latest_event FROM order_events;

-- Count events by hour
SELECT 
  EXTRACT(hour FROM timestamp) as hour,
  COUNT(*) as events
FROM order_events 
WHERE DATE(timestamp) = CURRENT_DATE
GROUP BY hour 
ORDER BY hour;

-- Detect anomalies (orders > 2 standard deviations from mean)
WITH stats AS (
  SELECT 
    AVG(amount) as mean_amount,
    STDDEV(amount) as std_amount
  FROM order_events
)
SELECT * 
FROM order_events, stats
WHERE amount > (mean_amount + 2 * std_amount)
   OR amount < (mean_amount - 2 * std_amount);
```

---

## Troubleshooting

### Common Issues

| Symptom | Potential Cause | Solution |
|---------|----------------|----------|
| **SSL handshake failed** | Missing or incorrect certificates | Verify `ca.pem`, `service.cert`, `service.key` are in project root with correct permissions |
| **No messages in PostgreSQL** | Consumer not running or configuration error | Check consumer logs, verify topic name and consumer group ID |
| **Connection timeout** | Network/firewall issues | Verify Aiven services have public access enabled |
| **Grafana shows no data** | Data source misconfigured | Test PostgreSQL connection in Grafana, check query syntax |
| **Producer stops sending** | Rate limiting or network issues | Check producer logs, verify Kafka service status |

### Debug Commands

```bash
# Test PostgreSQL connection
python -c "
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv('PG_URI'))
print('PostgreSQL connection successful!')
conn.close()
"

# Check Kafka topic
kafka-console-consumer --bootstrap-server $KAFKA_BOOTSTRAP \
  --topic order_events --from-beginning \
  --consumer-property security.protocol=SSL \
  --consumer-property ssl.ca.location=ca.pem \
  --consumer-property ssl.certificate.location=service.cert \
  --consumer-property ssl.key.location=service.key

# Verify table structure
psql $PG_URI -c "\d order_events"
```

### Logs and Monitoring

```bash
# Producer logs
tail -f producer.log

# Consumer logs  
tail -f consumer.log

# Check PostgreSQL logs in Aiven Console
# Monitor Kafka metrics in Aiven Console
```

---

## Next Steps & Extensions

### Immediate Improvements
- Add proper logging configuration
- Implement error handling and retry logic  
- Add data validation schemas
- Create health check endpoints

### Advanced Features
- **Docker Compose** for local development environment
- **Apache Airflow** for orchestrating batch jobs
- **Debezium CDC** for real database change streaming
- **Apache Flink** for complex event processing
- **Kubernetes** deployment manifests
- **Prometheus + AlertManager** for monitoring and alerting

### Production Ready
- Add authentication and authorization
- Implement data encryption at rest
- Set up automated backups
- Create disaster recovery procedures
- Add comprehensive monitoring and alerting
- Implement data retention policies

### ML & Analytics
- **Apache Spark** for batch analytics
- **MLflow** for machine learning experiments
- Anomaly detection algorithms
- Customer segmentation models
- Revenue forecasting

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `python -m pytest tests/`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Submit a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits & Acknowledgments

Built with care using:
- **[Aiven](https://aiven.io/)** - Managed Kafka & PostgreSQL services
- **[Grafana](https://grafana.com/)** - Visualization and dashboards  
- **[Faker](https://faker.readthedocs.io/)** - Realistic fake data generation
- **[Apache Kafka](https://kafka.apache.org/)** - Event streaming platform
- **[PostgreSQL](https://www.postgresql.org/)** - Powerful relational database

Special thanks to the open-source community for making these amazing tools available.

---

## Support

- **Email:** support@yourcompany.com
- **Slack:** [#data-engineering](https://yourworkspace.slack.com)
- **Issues:** [GitHub Issues](https://github.com/yourusername/real_time_pipeline/issues)
- **Wiki:** [Project Wiki](https://github.com/yourusername/real_time_pipeline/wiki)

---

<div align="center">

**If this project helped you, please give it a star!**

Made by [Your Name](https://github.com/yourusername)

</div>
