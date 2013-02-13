from socket import *
import struct
import platform


SSDP_MULTICAST_GROUP = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MULTICAST_TTL = 4 # > 1 traverses subnets.. possibly =)
    # TODO must be packed as a single byte.. struct.pack(b, SSDP_...TTL)

# Strategy:
# -----------------------
#  echo "NOTIFY * HTTP/1.1" | socat - UDP-DATAGRAM:192.168.1.173:2048
#
# TODO create a model for dealing with the SSDP protocol, without dealing with transport..
#
# - Listen for multicasts at 1900
# - add the concept of a control point, being able to search
#    - accept NOTIFY multicasts on 1900
#    - use a distinct socket for searches, i.e. not 1900, since the 200 OK replies are sent unicast, and possibly eaten by other sockets..
# - [root?]device's, responding to M-SEARCH'es must bind & reply to multicasts on 1900, and a different port for unicasts
#    - (spotify etc, only one socket receives the unicast)
#    - use the SEARCHPORT.UPNP.ORG header to specify the unicast search port, or simply say fucko to unicast searches..?
#

ME = '192.168.1.173'

class SSDPServer:
    # TODO docme
    
    def __init__(self):
        # TODO not even sure if this belongs here at all.. transport is irrelevant, resistance is futile..
        self.sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # multicasts
        #self.sock.bind(('', SSDP_PORT)) # TODO impossible to specify an interface???
        #self.sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP,
        #        struct.pack("4sl", inet_aton(SSDP_MULTICAST_GROUP), INADDR_ANY))
        
        # unicast
        #self.sock.bind((ME, SSDP_PORT + 1000)) # binding not necessary?


# TODO remove me
if __name__ == '__main__':
    s = SSDPServer()
    print(s)

    # testing to see if any replies are received...
    def req(to):
        # TODO MX _MUST_ be >= 1

        # TODO not all devices respond to ssdp:all ??
        # search_target='urn:schemas-upnp-org:device:MediaServer:1'
        # search_target='ssdp:all'
        search_target='upnp:rootdevice'

        return "M-SEARCH * HTTP/1.1\r\n"\
               "HOST: %s:%d\r\n"\
               "MAN: \"ssdp:discover\"\r\n"\
               "ST: %s\r\n"\
               "MX: 1\r\n"\
               "USER-AGENT: %s/%s UPnP/1.1 pyupnp/0.1\r\n"\
               "\r\n" % (to, SSDP_PORT, search_target, platform.system(), platform.release())
        
    s.sock.sendto(req(SSDP_MULTICAST_GROUP).encode(),
            (SSDP_MULTICAST_GROUP, SSDP_PORT))


    while True:
        data, (addr, port) = s.sock.recvfrom(4096)
        #print(addr, port, ':', data.decode())
        print(addr, port)


# TODO UDPServer + ThreadingMixIn??? server_bind can be overriden for the multicast stuff...

