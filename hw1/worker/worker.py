import socket
import logging
import os
import struct
import threading
import pickle
import time
from utils import serializers


TYPE = os.getenv("TYPE")
PORT = os.getenv("PORT")
COUNT_TESTS = os.getenv("COUNT_TESTS")
MLTCAST_GRP = os.getenv("MLTCAST_GRP")
MLTCAST_PORT = os.getenv("MLTCAST_PORT")
BUFF_SIZE = 1024

def getMsgToClient():
    ans = TYPE + " - "
    ser, deser = None, None
    if TYPE == "native":
        ser = serializers.native_to
        deser = serializers.native_from
    elif TYPE == "xml":
        ser = serializers.xml_to
        deser = serializers.xml_from
    elif TYPE == "json":
        ser = serializers.json_to
        deser = serializers.json_from
    elif TYPE == "proto":
        ser = serializers.proto_to
        deser = serializers.proto_from
    elif TYPE == "avro":
        ser = serializers.avro_to
        deser = serializers.avro_from
    elif TYPE == "yaml":
        ser = serializers.yaml_to
        deser = serializers.yaml_from
    elif TYPE == "msgpack":
        ser = serializers.msgpack_to
        deser = serializers.msgpack_from
    
    start_time = time.time()
    for i in range(int(COUNT_TESTS) - 1):
        ser()
    data = ser()
    ser_time = (time.time() - start_time) / int(COUNT_TESTS)

    sz = len(data)

    start_time = time.time()
    for i in range(int(COUNT_TESTS)):
        deser(data)
    deser_time = (time.time() - start_time) / int(COUNT_TESTS)

    ans += str(sz) + ' - ' + ("%.6f" % ser_time) + ' - ' + ("%.6f" % deser_time)
    return ans.encode('utf-8') + b'\n'

def multicastHandler():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((MLTCAST_GRP, int(MLTCAST_PORT)))
    mreq = struct.pack("4sL", socket.inet_aton(MLTCAST_GRP), socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    logging.info("Listen multicast port: %s", MLTCAST_PORT)

    while True:
        data, addr = s.recvfrom(BUFF_SIZE)
        s.sendto(getMsgToClient(), addr)


def unicastHandler():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((TYPE, int(PORT)))

    logging.info("Listen port: %s", PORT)

    while True:
        data, addr = s.recvfrom(BUFF_SIZE)
        s.sendto(getMsgToClient(), addr)




logging.basicConfig(level=logging.INFO)
t1 = threading.Thread(target=unicastHandler)
t2 = threading.Thread(target=multicastHandler)
for t in [t1, t2]: t.start()
for t in [t1, t2]: t.join()