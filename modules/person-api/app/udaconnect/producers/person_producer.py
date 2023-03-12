import json
import logging
from builtins import staticmethod

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-producer")

PERSON_TOPIC = 'person'
KAFKA_SERVER = 'kafka:9092'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class PersonProducer:
    @staticmethod
    def send_message(person):
        """
        Sends a message to Kafka's person creation topic

        :param location: person to be created
        :return:
        """
        kafka_producer.send(PERSON_TOPIC, json.dumps(person).encode())
        kafka_producer.flush(timeout=5.0)
