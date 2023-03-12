from app.udaconnect.consumers.person_topic_consumer import PersonTopicConsumer
from app.udaconnect.consumers.location_topic_consumer import LocationTopicConsumer

KAFKA_SERVER = 'kafka:9092'


if __name__ == "__main__":
    PersonTopicConsumer(kafka_server=KAFKA_SERVER).start()
    LocationTopicConsumer(kafka_server=KAFKA_SERVER).start()
