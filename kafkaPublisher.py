import ssl
import json
import random
import asyncio
from datetime import datetime
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to generate random JSON data
def generate_random_data():
    return json.dumps({
        "id": random.randint(1, 1000000),
        "timestamp": datetime.now().isoformat(),
        "value": random.random()
    })

# Kafka producer function to publish messages asynchronously
async def kafka_async_publisher():
    # Load producer-specific environment variables
    topic = os.getenv("KAFKA_PRODUCER_TOPIC")
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(",")
    sasl_username = os.getenv("KAFKA_SASL_USERNAME")
    sasl_password = os.getenv("KAFKA_SASL_PASSWORD")
    num_messages = int(os.getenv("KAFKA_NUM_MESSAGES"))

    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        security_protocol="SASL_SSL",
        sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM"),
        sasl_plain_username=sasl_username,
        sasl_plain_password=sasl_password,
        ssl_context=ssl.create_default_context(),
        linger_ms=5,  # Short delay to batch more messages
        compression_type='gzip',  # Compress messages for better performance
        max_request_size=1048576,  # 1MB, adjust if needed for larger messages
    )
    await producer.start()

    try:
        start_time = asyncio.get_event_loop().time()
        tasks = []

        # Produce messages
        for _ in range(num_messages):
            data = generate_random_data()
            tasks.append(producer.send_and_wait(topic, data.encode('utf-8')))

        # Wait for all messages to be published
        await asyncio.gather(*tasks)

        end_time = asyncio.get_event_loop().time()
        print(f"Published {num_messages} messages to {topic} in {end_time - start_time:.2f} seconds.")
    finally:
        await producer.stop()

# Kafka consumer function to consume messages asynchronously
async def kafka_async_listener():
    # Load consumer-specific environment variables
    group_id = os.getenv("KAFKA_CONSUMER_GROUP_ID")
    topic = os.getenv("KAFKA_CONSUMER_TOPIC")
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(",")
    sasl_username = os.getenv("KAFKA_SASL_USERNAME")
    sasl_password = os.getenv("KAFKA_SASL_PASSWORD")

    consumer = AIOKafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        security_protocol="SASL_SSL",
        sasl_mechanism=os.getenv("KAFKA_SASL_MECHANISM"),
        sasl_plain_username=sasl_username,
        sasl_plain_password=sasl_password,
        auto_offset_reset="earliest",
        ssl_context=ssl.create_default_context(),
    )
    await consumer.start()

    try:
        print(f"Consumer {group_id} is Waiting for messages...")
        async for message in consumer:
            print(f"Consumed message: {message.value}")
    finally:
        await consumer.stop()

# Main function to run the publisher and listener concurrently
async def main():
    # Run the publisher and consumer concurrently
    publisher_task = asyncio.create_task(kafka_async_publisher())
    listener_task = asyncio.create_task(kafka_async_listener())

    # Wait for both tasks to complete
    await asyncio.gather(publisher_task, listener_task)

if __name__ == "__main__":
    print("Starting Kafka Publisher and Consumer...")
    asyncio.run(main())
