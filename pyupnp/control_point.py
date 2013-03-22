import socketserver
import time # TODO rm?
import threading

from pyupnp.ssdp.protocol import *
from pyupnp.ssdp.transport import *

# TODO this isn't exactly a control point.. A control point is the client of this class.. This is more like
# the SSDP neighborhood, a record of the discovered devices/services... ?

class ControlPoint(object):
    """An UPnP control point, locating available devices and services."""

    def __init__(self):
        self._server = ControlPoint._SsdpBroadcastServer(self._on_message)
        self.search()

    def stop(self):
        # TODO docme
        self._server.shutdown()

    def search(self, target = 'ssdp:all', mx = 5):
        req = SearchRequest()
        req.set_headers(st = target) # TODO crap
        req.mx = mx

        search = threading.Thread(args=(req, self._on_message), target=_ssdp_search)
        search.daemon = True
        search.start()

    def _on_message(self, client, msg):
        # TODO remember synchronization when updating cached information
        print('Received message from', client)
        print(msg)
        print()
        print()
        # TODO return replies here as well?

    # TODO two separate ports, on for multicast adverts, one for uncast replies to M-SEARCH
        # TODO open/close new sockets on-demand instead of keeping one search-port open?


    # TODO send a search-request once started, and every 30sec?
    # TODO keep a list of devices/services, make it possible to query
    # TODO notify clients of updates (addition/removal of services?)
    # TODO search for specific devices/services ..?


    class _SsdpBroadcastServer(socketserver.UDPServer, socketserver.ThreadingMixIn):
        def __init__(self, callback):
            super(socketserver.UDPServer, self).__init__(SSDP_MULTICAST_ADDR, ControlPoint._RequestHandler)
            self.callback = callback
            self.server_thread = threading.Thread(target=self.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

        def server_bind(self):
            configure_ssdp_broadcast_server_socket(self.socket)

    class _RequestHandler(socketserver.BaseRequestHandler): # TODO generic request-handler, or broadcast-specific?
        def handle(self):
            # TODO log any failure to parse the message, override server.handle_error for this?
            msg = parse_ssdp_message(self.request[0].decode('utf-8'))
            self.server.callback(self.client_address, msg)


def _ssdp_search(req, callback): # TODO naming, at least =)
    s = create_ssdp_broadcast_client_socket()
    try:
        s.sendto(req.encode().encode('utf-8'), req.host)
        s.settimeout(1)
        while True: # TODO more like: time < mx * 2
            data, client = s.recvfrom(8192)
            callback(client, parse_ssdp_message(data.decode('utf-8')))

    # TODO error-logging?
    finally:
        s.close()

if __name__ == '__main__':
    cp = ControlPoint()
    print('Waiting for messages...')
    for x in range(5):
        print('.');
        time.sleep(1)

