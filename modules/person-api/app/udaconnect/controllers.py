from datetime import datetime
from typing import List, Optional

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields

from app.udaconnect.models.connection import Connection
from app.udaconnect.models.location import Location
from app.udaconnect.models.person import Person
from app.udaconnect.schemas import ConnectionSchema, PersonSchema
from app.udaconnect.services.connection_service import ConnectionService
from app.udaconnect.services.person_service import PersonService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect - Person API", description="Endpoints to provide person data")  # noqa

person_model = api.model('Person', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'company_name': fields.String
})

location_model = api.model('Location', {
        'id': fields.Integer,
        'person_id': fields.Integer,
        'longitude': fields.String,
        'latitude': fields.String,
        'creation_time': fields.DateTime
    })

connection_model = api.model('Connection', {
    'location': fields.Nested(location_model),
    'person': fields.Nested(person_model)
})


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @api.doc(description='Creates a new Person',
             body=person_model,
             responses={
                 202: 'Person has been successfully created',
                 500: 'Internal server error'
             }
             )
    def post(self):
        payload = request.get_json()
        PersonService.create(payload)

        return {'status': 'accepted'}, 202

    @responds(schema=PersonSchema, many=True)
    @api.doc(description='Retrieve all people',)
    @api.response(200, 'Successfully retrieved all people', fields.List(fields.Nested(person_model)))
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Id of a Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    @api.doc(description='Search for a given person by id',
             params={'person_id': 'Id(required) of the person to search'},
             responses={
                 404: 'Person not found',
                 500: 'Internal server error'
             },
             )
    @api.response(200, 'Person was found', person_model)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "start of date range", _in="query")
@api.param("end_date", "end of date range", _in="query")
@api.param("distance", "Proximity in meters", _in="query")
@api.doc(description='Searches for connection(s) of a given person',
         model=connection_model)
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    @api.response(200, 'Succesfully found connection(s)', fields.List(fields.Nested(connection_model)))
    def get(self, person_id) -> List[ConnectionSchema]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(
            request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=int(person_id),
            start_date=start_date,
            end_date=end_date,
            meters=float(distance)
        )

        connection_list: List[Connection] = [
            ConnectionDataResource.proto_to_person(connection)
            for connection in results.connections
        ]

        return connection_list

    @staticmethod
    def proto_to_person(connection) -> Connection:
        
        proto_person = connection.person
        actual_person = Person(id=proto_person.id,
                        first_name=proto_person.first_name,
                        last_name=proto_person.last_name,
                        company_name=proto_person.company_name)
        
        proto_location = connection.location
        actual_location = Location(id=proto_location.id,
                            person_id=proto_location.person_id,
                            wkt_shape=proto_location.wkt_shape,
                            creation_time=datetime.fromtimestamp(
                                proto_location.creation_time.seconds)
                            )

        return Connection(person=actual_person, location=actual_location)
