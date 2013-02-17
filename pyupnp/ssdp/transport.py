# TODO docme
"""
blah blah
"""

from socket import * # TODO fixo
import platform
import struct

from pyupnp.ssdp.protocol import *


SSDP_MULTICAST_GROUP = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MULTICAST_TTL = 2 # > 1 traverses subnets.. possibly =)
SSDP_USER_AGENT = "%s/%s UPnP/1.1 pyupnp/0.1" % (platform.system(), platform.release())


if __name__ == '__main__':
    search = True

    if not search:

        # init the socket for multicast listening
        s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('', SSDP_PORT)) # TODO CANNOT BIND TO ANY INTERFACE.. IS THAT REALLY CORRECT??
        s.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP,
                struct.pack("=4sl", inet_aton(SSDP_MULTICAST_GROUP), INADDR_ANY))

    else:
        req = SearchRequest()
        # TODO sane defaults please
        # TODO proper setters?
        req.headers['host'] = '%s:%d' % (SSDP_MULTICAST_GROUP, SSDP_PORT)
        req.headers['man'] = '"ssdp:discover"'
        req.headers['mx'] = '1'
        req.headers['st'] = 'ssdp:all'
        #req.headers['st'] = 'upnp:rootdevice'
        req.headers['user-agent'] = SSDP_USER_AGENT
        print('Sending %s' % req)
        print()

        # init the socket for multicast sending
        s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        s.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, SSDP_MULTICAST_TTL)

        # send the request
        s.sendto(req.encode().encode('utf-8'), (SSDP_MULTICAST_GROUP, SSDP_PORT))

    # Await replies
    while True:
        data, (addr, port) = s.recvfrom(4096)
        print("Msg from", addr, port)
        print(parse_ssdp_message(data.decode('utf-8')))
        print()
        print()
