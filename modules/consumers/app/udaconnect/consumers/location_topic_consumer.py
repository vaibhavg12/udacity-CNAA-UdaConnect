import json
import logging
import threading

from app.udaconnect.services.location_consumer_service import LocationConsumerService
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-topic-consumer")

LOCATION_TOPIC = 'location'

class LocationTopicConsumer(threading.Thread):
    """
    location topic consumer.
    referenced from
    https://github.com/dpkp/kafka-python/blob/master/example.py
    """
    def __init__(self, kafka_server):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.kafka_server = kafka_server

    def stop(self):
        self.stop_event.set()

    def run(self):
        logger.info('----Starting Location Topic Consumer----')

        consumer = KafkaConsumer(bootstrap_servers=self.kafka_server,
                                 consumer_timeout_ms=1000,
                                 group_id='location-group')
        consumer.subscribe(LOCATION_TOPIC)

        while not self.stop_event.is_set():
            for message in consumer:
                LocationConsumerService.create(
                    json.loads(message.value.decode('utf-8'))
                )
                if self.stop_event.is_set():
                    break

        logger.info('----Stopping Location Topic Consumer----')
        consumer.close()
