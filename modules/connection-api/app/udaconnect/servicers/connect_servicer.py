import logging
from datetime import datetime

from app.udaconnect.proto.connect_pb2_grpc \
    import ConnectMessageServiceServicer
from app.udaconnect.services.connection_service import ConnectionService

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-connection-servicer")


class ConnectServicer(ConnectMessageServiceServicer):

    def FindConnections(self, request, context):
        """
        Delegate implementation for finding connect data between two
        selected persons (person_id) that share geo location proximity.

        :param request: SearchMessage request data for retrieving connection(s), if any
        :param context: gRPC context
        :return: Returns a List that has all the ConnectMessages(s)
        instances found
        """

        params = {
            'start_date': datetime.fromtimestamp(request.start_date.seconds),
            'end_date': datetime.fromtimestamp(request.end_date.seconds),
            'person_id': int(request.person_id),
            'meters': float(request.meters)
        }

        connections = ConnectionService.find_contacts(**params)

        return connections
