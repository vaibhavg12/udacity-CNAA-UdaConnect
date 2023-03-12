import json
import logging

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-producer")

LOCATION_TOPIC = 'location'
KAFKA_SERVER = 'kafka:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class LocationProducer:
    @staticmethod
    def send_message(location):
        """
        Sends a message to Kafka's location creation topic

        :param location: location to be created
        :return:
        """
        producer.send(LOCATION_TOPIC, json.dumps(location).encode())
        producer.flush(timeout=5.0)
