import logging

from typing import Dict

from app.udaconnect.infra.database import DBSession
from app.udaconnect.models.person import Person
from app.udaconnect.models.schemas import PersonSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-consumer-service")

session = DBSession()


class PersonConsumerService:
    @staticmethod
    def create(person: Dict):
        """
        consumes a person and saves it to database.

        :param person: a person
        """
        
        validate_person: Dict = PersonSchema().validate(person)
        if validate_person:
            logger.warning(
                f"Payload is in invalid format: {person}")
            raise Exception(f"Payload is invalid: {person}")

        to_be_saved = Person()
        to_be_saved.first_name = person["first_name"]
        to_be_saved.last_name = person["last_name"]
        to_be_saved.company_name = person["company_name"]

        session.add(to_be_saved)
        session.commit()

        logger.info(f"Person :: {to_be_saved.id} has been saved to database")
        
