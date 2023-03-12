from datetime import datetime, timedelta
from typing import List

from app.udaconnect.infra.database import DBSession, engine
from app.udaconnect.proto.connect_pb2 import PersonMessage as PersonPB2, \
    LocationMessage as LocationPB2, ConnectMessage, ConnectMessages
from app.udaconnect.services.location_service import LocationService
from app.udaconnect.services.person_service import PersonService
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.sql import text

session = DBSession()

class ConnectionService:

    @staticmethod
    def person_to_proto(person) -> PersonPB2:
        """
        Utililty method to transform a person to protobuf person model.
        :param person: Person model 
        :return: PersonPB2
        """

        return PersonPB2(id=person.id, first_name=person.first_name,
                         last_name=person.last_name,
                         company_name=person.company_name)

    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime,
                      meters=5) -> ConnectMessages:
        """
        Finds all Person who have been within a given distance of a given
        Person within a date range.

        :param person_id: Person id to look for contacts
        :param start_date: The start date for looking for contacts
        :param end_date: The end date for looking for contacts
        :param meters: The distance to check for proximity. Default: 5
        """

        locations: List = LocationService.retrieve_person_locations(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date
        )

        # Prepare arguments for queries
        data = []
        for location in locations:
            f_end_date = (end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": f_end_date,
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate),
                ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin
            (coordinate::geography,ST_SetSRID
                (ST_MakePoint(:latitude,:longitude),4326)::geography,
            :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        connection_list = ConnectMessages()
        result: List[ConnectMessage] = []
        for line in tuple(data):
            for (
                    exposed_person_id,
                    location_id,
                    exposed_lat,
                    exposed_long,
                    exposed_time,
            ) in engine.execute(query, **line):
                location = LocationPB2(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=Timestamp(
                        seconds=int(exposed_time.timestamp())
                    ),
                )
                location.wkt_shape = \
                    f"ST_POINT({exposed_lat} {exposed_long})"

                result.append(
                    ConnectMessage(
                        person=ConnectionService.person_to_proto(
                            PersonService.retrieve(exposed_person_id)
                        ), location=location
                    )
                )

        connection_list.connections.extend(result)

        return connection_list
