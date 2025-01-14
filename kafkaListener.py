import asyncio
import ssl
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Task to simulate moderate complexity work
def perform_task(message):
    print(f"Processed message: {message.value}")

# Function to consume Kafka messages asynchronously
async def kafka_async_listener(executor):
    group_id = os.getenv("KAFKA_GROUP_ID")
    topic = os.getenv("KAFKA_TOPIC")
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(",")
    sasl_mechanism = os.getenv("KAFKA_SASL_MECHANISM")
    sasl_plain_username = os.getenv("KAFKA_SASL_USERNAME")
    sasl_plain_password = os.getenv("KAFKA_SASL_PASSWORD")

    consumer = AIOKafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        security_protocol="SASL_SSL",
        sasl_mechanism=sasl_mechanism,
        sasl_plain_username=sasl_plain_username,
        sasl_plain_password=sasl_plain_password,
        auto_offset_reset="earliest",
        ssl_context=ssl.create_default_context(),
    )
    await consumer.start()

    try:
        print(f"Consumer {group_id} is Waiting for messages...")
        async for message in consumer:
            loop = asyncio.get_event_loop()
            loop.run_in_executor(executor, perform_task, message)
    finally:
        await consumer.stop()

# Function to create multiple consumers with the same group ID
async def start_multiple_consumers(executor, num_consumers=20):
    tasks = []
    for _ in range(num_consumers):
        tasks.append(kafka_async_listener(executor=executor))
    await asyncio.gather(*tasks)

# Main function to launch multiple consumers
async def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        await start_multiple_consumers(executor=executor)

if __name__ == "__main__":
    print("Start DLMS Server...")
    asyncio.run(main())
