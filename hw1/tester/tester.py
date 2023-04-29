
import socket
import logging
import os


PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_ADDRESS = ("proxy", int(PROXY_PORT))
TYPES = ['native', 'xml', 'json', 'avro', 'yaml', 'msgpack', 'proto', 'all']
BUFFER_SIZE   = 1024

logging.basicConfig(level=logging.INFO)
for type in TYPES:
    msgToProxy = bytes('get_result ' + type, 'utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.sendto(msgToProxy, PROXY_ADDRESS)
        msgFromServer, addr = s.recvfrom(BUFFER_SIZE)
        msg = "Message from Server :\n {0}".format(msgFromServer.decode('utf-8'))
        logging.info(msg)