from confluent_kafka import Producer
from faker import Faker
import json, time

fake = Faker()

conf = {
    'bootstrap.servers': 'kafka-15300c97-data2.c.aivencloud.com:17974',
    'security.protocol': 'SSL',
    'ssl.ca.location': 'ca.pem',
    'ssl.certificate.location': 'service.cert',
    'ssl.key.location': 'service.key'
}

producer = Producer(conf)

def produce_order():
    order = {
        "order_id": fake.uuid4(),
        "customer": fake.name(),
        "amount": round(fake.random_number(digits=4), 2),
        "timestamp": fake.iso8601()
    }
    producer.produce("order_events", value=json.dumps(order))
    producer.flush()
    print("Produced:", order)

while True:
    produce_order()
    time.sleep(2)
