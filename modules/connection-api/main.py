import logging
import grpc
import os
import time

from concurrent import futures

from app.udaconnect.servicers.connect_servicer import ConnectServicer
from app.udaconnect.proto.connect_pb2_grpc import add_ConnectMessageServiceServicer_to_server


SERVER_PORT = os.environ.get("GRPC_PORT") or 5005

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
add_ConnectMessageServiceServicer_to_server(ConnectServicer(), server)
server.add_insecure_port(f"[::]:{SERVER_PORT}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-connect-data")
logger.info(f"Starting udaconnect-connect-data server on port :: {SERVER_PORT}")

server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
