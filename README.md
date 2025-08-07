# Real-Time Data Pipeline with Aiven Kafka and PostgreSQL

A beginner-friendly project that demonstrates how to build a real-time data streaming pipeline using Aiven's managed services.

## Overview

This project simulates e-commerce order events and processes them in real-time through a streaming pipeline. The system generates fake order data, streams it through Kafka, and stores the processed data in PostgreSQL for analysis.

**Architecture:** Python Producer → Aiven Kafka → Python Consumer → Aiven PostgreSQL

## Prerequisites

- Python 3.x
- Aiven account (free tier available)
- Basic understanding of Python and SQL

## Required Python Packages

```bash
pip install confluent_kafka faker psycopg2-binary
```

## Setup Instructions

### 1. Create Aiven Services

**Kafka Service:**
- Create a new Kafka service in Aiven Console
- Enable Karapace REST API
- Configure public access or whitelist your IP
- Download SSL certificates (ca.pem, service.cert, service.key)

**PostgreSQL Service:**
- Create a PostgreSQL service
- Enable public access
- Note the connection URI for later use

### 2. Create Database Table

Connect to your PostgreSQL instance and run:

```sql
CREATE TABLE order_events (
    id SERIAL PRIMARY KEY,
    order_id TEXT,
    customer TEXT,
    amount FLOAT,
    timestamp TEXT
);
```

### 3. Create Kafka Topic

In the Aiven Console:
- Navigate to your Kafka service
- Go to Topics section
- Create a new topic named `order_events`

## Usage

### Running the Producer

The producer generates fake order data and sends it to Kafka:

```bash
python producer.py
```

### Running the Consumer

The consumer reads from Kafka and stores data in PostgreSQL:

```bash
python consumer.py
```

### Verifying Data

Query PostgreSQL to see the processed orders:

```sql
SELECT * FROM order_events ORDER BY id DESC LIMIT 10;
```

## Project Structure

```
real_time_pipeline/
├── producer.py          # Generates and sends order events
├── consumer.py          # Consumes events and stores in DB
├── ca.pem              # SSL certificate
├── service.cert        # SSL certificate
├── service.key         # SSL private key
└── README.md           # This file
```

## Configuration

Update the connection details in both Python scripts:

- Replace `<AIVEN_KAFKA_URL>` with your Kafka bootstrap servers
- Update PostgreSQL connection parameters with your service details
- Ensure SSL certificate files are in the project directory

## Features

- Real-time data streaming
- Automatic fake data generation
- SSL-secured connections
- Error handling and graceful shutdown
- Scalable architecture using managed services

## Next Steps

- Connect PostgreSQL to visualization tools (Grafana, Metabase)
- Add data transformation logic in the consumer
- Implement schema registry for better data governance
- Scale up with multiple consumers for parallel processing

## Troubleshooting

**Connection Issues:**
- Verify SSL certificates are correctly placed
- Check network access settings in Aiven Console
- Confirm service URLs and credentials

**No Data Flow:**
- Ensure Kafka topic exists
- Check consumer group configuration
- Verify producer is successfully sending messages

## License

MIT License - feel free to use this project for learning and development.
