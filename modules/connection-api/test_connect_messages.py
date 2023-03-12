import grpc
import os
import sys

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.proto.connect_pb2_grpc import ConnectMessageServiceStub
from app.udaconnect.proto.connect_pb2 import SearchMessage


def validate_arguments(arguments):
    """
        validates the input arguments

        :param arguments: arguments to be validated
        :return: validated arguments
    """
    arguments_count = len(arguments)

    if arguments_count not in range(3, 5):
        print(f"Invalid arguments received: Expected arguments are 3 ~ 4 / but received {arguments_count}")
        print("USING: ")
        print("\t$ python test_connections.py 6 2020-01-01 2020-06-30 [5]\n")

        raise ValueError("Invalid number of arguments received")

    person_id = int(arguments[0])
    start_date = arguments[1].split("-")
    end_date = arguments[2].split("-")
    distance_in_mts = None

    if len(start_date) != 3:
        raise ValueError(f"Invalid start date: {sys.argv[2]}")

    if len(end_date) != 3:
        raise ValueError(f"Invalid end date: {sys.argv[2]}")
   
    if arguments_count == 4:
        distance_in_mts = float(arguments[3])
  
    return person_id, start_date, end_date, distance_in_mts


if __name__ == '__main__':

    grpc_host = os.environ.get('GRPC_HOST') or 'localhost:30003'
    grpc_channel = grpc.insecure_channel(grpc_host)
   
    stub = ConnectMessageServiceStub(grpc_channel)

    person_id, start_date, end_date, distance = validate_arguments(sys.argv[1:])

    start = datetime(year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2]))
    end = datetime(year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2]))

    start_millis = Timestamp(seconds=int(start.timestamp()))
    end_millis = Timestamp(seconds=int(end.timestamp()))

    search_msg = SearchMessage(person_id=person_id,
                               start_date=start_millis,
                               end_date=end_millis,
                               meters=distance)

    print(f"Sending search message :: {search_msg} to host :: {grpc_host}")
    response = stub.FindConnections(search_msg)

    print(f"Response from host :: {response}")
