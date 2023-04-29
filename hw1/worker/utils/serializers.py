import pickle
import jsonpickle
from xml_marshaller import xml_marshaller
from io import BytesIO
import fastavro
import yaml
from utils import object_pb2
import msgpack


class Object:
    def __init__(self):
        self.i = 123
        self.big_i = 2^17
        self.f = 2.04
        self.m = {
            "key1": 1,
            "key2": 2
        }
        self.a = [1, 2, 3, 4] * 80
        self.s = "str" * 100

object = Object()

object_schema = {
    "namespace": "example.avro",
    "type": "record",
    "name": "object",
    "fields": [
        {"name": "i", "type": "int"},
        {"name": "big_i", "type": "int"},
        {"name": "f", "type": "float"},
        {"name": "m", "type": {"type": "map", "values": "int"}},
        {"name": "a", "type": {"type": "array", "items": "int"}},
        {"name": "s", "type": "string"},
    ]
}

def native_to():
    return pickle.dumps(object)

def native_from(data):
    pickle.loads(data)

def xml_to():
    return xml_marshaller.dumps(object)

def xml_from(data):
    xml_marshaller.loads(data)

def json_to():
    return jsonpickle.encode(object)

def json_from(data):
    jsonpickle.decode(data)

def avro_to():
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, object_schema, object.__dict__)
    return bytes_writer.getvalue()

def avro_from(data):
    bytes_writer = BytesIO()
    bytes_writer.write(data)
    bytes_writer.seek(0)
    fastavro.schemaless_reader(bytes_writer, object_schema)

def yaml_to():
    return yaml.dump(object)

def yaml_from(data):
    yaml.load(data, Loader=yaml.Loader)

def msgpack_to():
    return msgpack.packb(object, default=lambda x: list(x.__dict__.values()))

def msgpack_from(data):
    msgpack.unpackb(data, strict_map_key=False)

def proto_to():
    proto_object = object_pb2.Object()
    proto_object.i = object.i
    proto_object.big_i = object.big_i
    proto_object.f = object.f
    for key in object.m:
        proto_object.m[key] = object.m[key]
    proto_object.a.extend(object.a)
    proto_object.s = object.s
    return proto_object.SerializeToString()

def proto_from(data):
    proto_object = object_pb2.Object()
    proto_object.ParseFromString(data)
    return
