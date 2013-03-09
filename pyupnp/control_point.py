import socketserver

from pyupnp.ssdp.protocol import *
from pyupnp.ssdp.transport import *


# TODO this isn't exactly a control point.. A control point is the client of this class.. This is more like
# the SSDP neighborhood, a record of the discovered devices/services... ?

class ControlPoint(object):
    """An UPnP control point, locating available devices and services."""

    def __init__(self):
        # TODO start the server here??
        pass

    def on_message(self, client, msg):
        print('Received message from', client)
        print(msg)
        print()
        print()
        # TODO return replies here as well?

    # TODO two separate ports, on for multicast adverts, one for uncast replies to M-SEARCH


    # TODO send a search-request once started, and every 30sec?
    # TODO keep a list of devices/services, make it possible to query
    # TODO notify clients of updates (addition/removal of services?)
    # TODO search for specific devices/services ..?


class _ControlPointUdpServer(socketserver.UDPServer, socketserver.ThreadingMixIn):

    def server_bind(self):
        configure_ssdp_broadcast_server_socket(self.socket)

class _ControlPointRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # TODO log any failure to parse the message
        msg = parse_ssdp_message(self.request[0].decode('utf-8'))
        self.server.cp.on_message(self.client_address, msg)


if __name__ == '__main__':
    cp = ControlPoint()

    server = _ControlPointUdpServer(SSDP_MULTICAST_ADDR, _ControlPointRequestHandler)
    server.cp = cp # TODO need to invert this.. the cp creates the server
    server.serve_forever()

    # TODO alternative...
    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.daemon = True
    # server_thread.start()
    # server.shutdown()

