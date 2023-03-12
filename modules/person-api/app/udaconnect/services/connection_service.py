import grpc
import logging

from builtins import staticmethod
from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.proto.connect_pb2_grpc import ConnectMessageServiceStub
from app.udaconnect.proto.connect_pb2 import SearchMessage

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-svc")


channel = grpc.insecure_channel("connection-api:5005")
stub = ConnectMessageServiceStub(channel)


class ConnectionService:

    @staticmethod
    def find_contacts(person_id, start_date, end_date, meters):
        """
        finds connected contacts of a give person

        :param person_id: unique id of person
        :param start_date: start date 
        :param end_date: end date
        :param meters: proximity distance in meters

        :return: list of connections
        """
        
        start_in_millis = Timestamp(seconds=int(start_date.timestamp()))
        end_in_millis = Timestamp(seconds=int(end_date.timestamp()))

        search_message = SearchMessage(person_id=person_id,
                                   start_date=start_in_millis,
                                   end_date=end_in_millis,
                                   meters=meters)

        response = stub.FindConnections(search_message)

        return response
