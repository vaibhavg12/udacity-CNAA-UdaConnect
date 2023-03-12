import logging

from geoalchemy2.functions import ST_Point
from typing import Dict

from app.udaconnect.infra.database import DBSession
from app.udaconnect.models.location import Location
from app.udaconnect.models.schemas import LocationSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-consumer-service")

session = DBSession()


class LocationConsumerService:
    @staticmethod
    def create(location: Dict):
        """
        consumes a location and saves it to database.
        
        :param location: a location
        """

        validate_location: Dict = LocationSchema().validate(location)
        if validate_location:
            logger.warning(
                f"Payload is in invalid format: {validate_location}")
            raise Exception(f"Payload is invalid: {validate_location}")

        to_be_saved = Location()
        to_be_saved.person_id = location["person_id"]
        to_be_saved.coordinate = ST_Point(
            location["latitude"], location["longitude"])
       
        session.add(to_be_saved)
        session.commit()

        logger.info(f"Location :: {to_be_saved.id} has been saved to database")
