import socket
import logging
import os


HOST = "proxy"
PORT = os.getenv("PORT")
MLTCAST_GRP = os.getenv("MLTCAST_GRP")
MLTCAST_PORT = os.getenv("MLTCAST_PORT")
SERVERS_PORT = os.getenv("SERVERS_PORT")
TYPES = [b'native', b'xml', b'json', b'proto', b'avro', b'yaml', b'msgpack', b'all']
BUFF_SIZE = 1024

logging.basicConfig(level=logging.INFO)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
s.bind((HOST, int(PORT)))

logging.info("Listen port: %s", PORT)

while True:
    data, addr = s.recvfrom(BUFF_SIZE)
    data = data.strip(b'\n')
    data = data.split(b' ')
    logging.debug("%s", data)
    if len(data) <= 1 or data[1] not in TYPES:
        continue

    if data[1] == b'all':
        logging.info("multicast")
        s.sendto(b'get', (MLTCAST_GRP, int(MLTCAST_PORT)))
        data = b''
        for _ in range(len(TYPES) - 1):
            tmp, _ = s.recvfrom(BUFF_SIZE)
            data += tmp
    else:
        logging.info("unicast")
        s.sendto(b'get', (data[1].decode('utf-8'), int(SERVERS_PORT)))
        data, _ = s.recvfrom(BUFF_SIZE)
    s.sendto(data, addr)
