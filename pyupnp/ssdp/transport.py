# TODO docme
"""
blah blah
"""

from socket import * # TODO fixo
import platform
import struct
import time

from pyupnp.ssdp.protocol import *


SSDP_MULTICAST_TTL = 2


def create_ssdp_broadcast_server_socket():
    """Returns a socket configured to receive broadcasted SSDP messages."""
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    return configure_ssdp_broadcast_server_socket(s)

def configure_ssdp_broadcast_server_socket(socket):
    """Configures an existing socket for receiving broadcasted SSDP messages."""
    socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socket.bind(('', SSDP_MULTICAST_ADDR[1]))
    socket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP,
        struct.pack("=4sl", inet_aton(SSDP_MULTICAST_ADDR[0]), INADDR_ANY))
    return socket

def create_ssdp_broadcast_client_socket():
    """Returns a socket configured to broadcast SSDP messages."""
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, SSDP_MULTICAST_TTL)
    return s


if __name__ == '__main__':
    search = True

    if not search:
        s = create_ssdp_broadcast_server_socket()

    else:
        req = SearchRequest()
        req.mx = 10
        print('Sending %s to %s' % (req, req.host))
        print()
        time.sleep(2)

        s = create_ssdp_broadcast_client_socket()
        s.sendto(req.encode().encode('utf-8'), req.host)

    # Await replies
    while True:
        data, (addr, port) = s.recvfrom(4096)
        print("Msg from", addr, port)
        print(parse_ssdp_message(data.decode('utf-8')))
        print()
        print()

