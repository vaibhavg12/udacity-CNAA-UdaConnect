from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectMessage(_message.Message):
    __slots__ = ["location", "person"]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PERSON_FIELD_NUMBER: _ClassVar[int]
    location: LocationMessage
    person: PersonMessage
    def __init__(self, location: _Optional[_Union[LocationMessage, _Mapping]] = ..., person: _Optional[_Union[PersonMessage, _Mapping]] = ...) -> None: ...

class ConnectMessages(_message.Message):
    __slots__ = ["connections"]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ConnectMessage]
    def __init__(self, connections: _Optional[_Iterable[_Union[ConnectMessage, _Mapping]]] = ...) -> None: ...

class LocationMessage(_message.Message):
    __slots__ = ["creation_time", "id", "latitude", "longitude", "person_id", "wkt_shape"]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    PERSON_ID_FIELD_NUMBER: _ClassVar[int]
    WKT_SHAPE_FIELD_NUMBER: _ClassVar[int]
    creation_time: _timestamp_pb2.Timestamp
    id: int
    latitude: str
    longitude: str
    person_id: int
    wkt_shape: str
    def __init__(self, id: _Optional[int] = ..., person_id: _Optional[int] = ..., longitude: _Optional[str] = ..., latitude: _Optional[str] = ..., creation_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., wkt_shape: _Optional[str] = ...) -> None: ...

class PersonMessage(_message.Message):
    __slots__ = ["company_name", "first_name", "id", "last_name"]
    COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    company_name: str
    first_name: str
    id: int
    last_name: str
    def __init__(self, id: _Optional[int] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., company_name: _Optional[str] = ...) -> None: ...

class SearchMessage(_message.Message):
    __slots__ = ["end_date", "meters", "person_id", "start_date"]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    METERS_FIELD_NUMBER: _ClassVar[int]
    PERSON_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    end_date: _timestamp_pb2.Timestamp
    meters: float
    person_id: int
    start_date: _timestamp_pb2.Timestamp
    def __init__(self, person_id: _Optional[int] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., meters: _Optional[float] = ...) -> None: ...
