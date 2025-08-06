from confluent_kafka import Consumer
import psycopg2
import json

# Kafka config
kafka_conf = {
    'bootstrap.servers': 'kafka-15300c97-data2.c.aivencloud.com:17974',
    'security.protocol': 'SSL',
    'ssl.ca.location': 'ca.pem',
    'ssl.certificate.location': 'service.cert',
    'ssl.key.location': 'service.key',
    'group.id': 'order_group',
    'auto.offset.reset': 'earliest'
}

# PostgreSQL config
pg_conn = psycopg2.connect(
    dbname="data_db",
    user="peter",
    password="1234",
    host="localhost",
    port=5432,
    sslmode='require'
)

cursor = pg_conn.cursor()

consumer = Consumer(kafka_conf)
consumer.subscribe(["order_events"])

print("Consumer started...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error():
            print("Error:", msg.error())
            continue

        order = json.loads(msg.value().decode('utf-8'))
        print("Consumed:", order)

        cursor.execute(
            "INSERT INTO order_events (order_id, customer, amount, timestamp) VALUES (%s, %s, %s, %s)",
            (order['order_id'], order['customer'], order['amount'], order['timestamp'])
        )
        pg_conn.commit()
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    consumer.close()
    pg_conn.close()
