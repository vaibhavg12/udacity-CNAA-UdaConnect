from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields

from app.udaconnect.models.location import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services.location_service import LocationService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect - Location API", description="Endpoints to provide location data")  # noqa

location_res = api.model('Location', {
    'id': fields.Integer,
    'person_id': fields.Integer,
    'longitude': fields.String,
    'latitude': fields.String,
    'creation_time': fields.DateTime
})


@api.route("/locations")
class LocationListResource(Resource):

    @accepts(schema=LocationSchema)
    @api.doc(description='Creates a new location Location',
             body=location_res,
             responses={
                202: 'Location has been successfully created',
                500: 'Internal server error'
                }
             )
    def post(self):
        location: Location = request.get_json()

        LocationService.create(location)

        return {'status': 'accepted'}, 202


@api.route("/locations/<location_id>")
@api.param("location_id", "Id of a Location", _in="query")
class LocationResource(Resource):

    @responds(schema=LocationSchema)
    @api.doc(description='Searches for a given location by id',
             params={'location_id': 'Id(required) of the location to search'},
             responses={
                 404: 'Location not found',
                 500: 'Internal server error'
                 },
             )
    @api.response(200, 'Location was found', location_res)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
