# Kafka Listener and Producer

This repository contains an asynchronous Kafka listener and producer implementation in Python using the `aiokafka` library. The producer sends messages to a Kafka topic, while the listener consumes messages from the topic.

## Prerequisites

1. **Python**: Ensure Python 3.7 or higher is installed.
   ```bash
   python --version
   ```
2. **Kafka Cluster**: Have a Kafka cluster running locally or remotely. Install Kafka locally or use a managed Kafka service.
3. **Install Dependencies**:
   - Use `pip` to install required Python packages.
     ```bash
     pip install -r requirements.txt
     ```

## File Structure

```plaintext
.
├── kafkaListener.py  # Kafka listener implementation
├── kafkaPublisher.py # Kafka producer implementation
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## Usage

### Kafka Producer

The Kafka producer (`kafkaPublisher.py`) sends messages to a Kafka topic asynchronously.

#### Configuration
- Update the following fields in the `kafkaPublisher.py` script:
  ```python
  topic = "<your-topic-name>"
  bootstrap_servers = ["<your-bootstrap-server>"]
  sasl_username = "<your-username>"
  sasl_password = "<your-password>"
  num_messages = <number-of-messages-to-send>
  ```

#### Run the Producer
```bash
python kafkaPublisher.py
```

### Kafka Listener

The Kafka listener (`kafkaListener.py`) consumes messages from a Kafka topic asynchronously.

#### Configuration
- Update the following fields in the `kafkaListener.py` script:
  ```python
  topic = "<your-topic-name>"
  bootstrap_servers = ["<your-bootstrap-server>"]
  sasl_username = "<your-username>"
  sasl_password = "<your-password>"
  ```

#### Run the Listener
```bash
python kafkaListener.py
```

## Requirements

The dependencies for this project are listed in the `requirements.txt` file:

```plaintext
aiokafka==0.8.0
asyncio
```

Install them using:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

1. **Cannot Allocate Memory**:
   - Close unnecessary applications to free up memory.
   - Increase system memory or swap space.

2. **Kafka Connection Error**:
   - Ensure the Kafka broker is running.
   - Verify the `bootstrap_servers` and broker configurations.

3. **SSL Configuration**:
   - Ensure your Kafka server supports `SASL_SSL` and your credentials are correct.

### Checking Kafka Logs
If errors persist, check the Kafka server logs for additional debugging information.

```bash
cat /path/to/kafka/logs/server.log
```

## License
This project is licensed under the MIT License.
