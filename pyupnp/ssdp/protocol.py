# TODO docme
"""
# TODO, PEP 257 sez..
The docstring for a module should generally list the classes, exceptions
and functions (and any other objects) that are exported by the module,
with a one-line summary of each. (These summaries generally give less detail
than the summary line in the object's docstring.) The docstring for a package
(i.e., the docstring of the package's __init__.py module) should also
list the modules and subpackages exported by the package.
"""

from pprint import pformat
import platform

SSDP_MULTICAST_ADDR = '239.255.255.250:1900'
# TODO harcoded version string..
SSDP_USER_AGENT = '%s/%s UPnP/1.1 pyupnp/0.1' % (platform.system(), platform.release())


def parse_ssdp_message(msg_string):
    """Parse an SSDP message provided as text."""
    startline, *header_lines = filter(None, msg_string.splitlines())
    
    msgtype = MESSAGE_TYPES.get(startline)
    if msgtype is None:
        raise ParsingError('Invalid SSDP start-line "%s"' % startline)
  
    headers = [(k.upper(), v.strip()) for (k, s, v) in
            [l.partition(':') for l in header_lines]]

    return msgtype.from_headers(dict(headers))


class SSDPMessage(object):
    """Base class for SSDP messages."""

    @classmethod
    def from_headers(cls, headers):
        """Create a new message based on headers provided in a dict."""
        msg = cls()
        msg._headers = {}
        for (k, v) in headers.items():
            parser = 'parse_' + _propname(k)
            if hasattr(msg, parser):
                try:
                    getattr(msg, parser)(v)
                except Exception as e:
                    raise ParsingError('Unable to parse %s=%s - %s' % (k, v, e))
            else:
                msg.set_headers(**{k: v})
        return msg

    def __init__(self):
        self._headers = dict(self._defaults())

    def __repr__(self):
        return (self.__class__.__name__ + ' '
                + pformat(_drop_empty_values(self._headers)))

    def set_headers(self, **headers):
        """Stores key/value pairs as headers."""
        for k, v in headers.items():
            self._headers[k.upper()] = v

    def get_header(self, k):
        """Returns the value of a header, or None"""
        return self._headers.get(k.upper())

    def encode(self):
        """Encodes the message as a string ready for transport"""
        hdrs = ['%s: %s' % (k, v) for k, v in _items_sorted_by_key(self._headers)]
        return "%s\r\n%s\r\n" % (self.__class__.START_LINE, '\r\n'.join(hdrs))


class SearchRequest(SSDPMessage):
    """An SSDP search request, issued to locate devices and services."""
    START_LINE = 'M-SEARCH * HTTP/1.1'

    def __init__(self):
        super(SearchRequest, self).__init__()

    @property
    def host(self):
        # TODO docme
        val = self.get_header('host')
        if val == None:
            return None
        addr, port = val.split(':')
        return (addr, int(port))
        # TODO seems to be some duplicaton going on here.. parse + property = overkill?

    @host.setter
    def host(self, value):
        addr, port = value
        self.set_headers(host = addr + ':' + port)

    def parse_host(self, value):
        self.host = value.split(':')

    @property
    def mx(self):
        """The number of seconds that the control point will wait for replies."""
        val = self.get_header('mx')
        return None if val == None else int(val)

    @mx.setter
    def mx(self, value):
        if int(value) <= 0:
            raise IllegalValueError('MX (%s) must be > 0' % value)
        self.set_headers(mx = str(value))

    def parse_mx(self, value):
        self.mx = value

    # TODO search target property

    def _defaults(self):
        return {
            'HOST': SSDP_MULTICAST_ADDR,
            'MAN': '"ssdp:discover"',
            'MX': '1',
            'ST': 'ssdp:all',
            'USER-AGENT': SSDP_USER_AGENT
        }


class SearchResponse(SSDPMessage):
    """The response to an SSDP search request."""
    START_LINE = 'HTTP/1.1 200 OK'

    def __init__(self):
        super(SearchResponse, self).__init__()

    def _defaults(self):
        return {} # TODO

    # TODO
    # HTTP/1.1 200 OK
    # CACHE-CONTROL: max-age = seconds until advertisement expires
    # DATE: when response was generated
    # EXT:
    # LOCATION: URL for UPnP description for root device
    # SERVER: OS/version UPnP/1.1 product/version
    # ST: search target
    # USN: composite identifier for the advertisement
    # BOOTID.UPNP.ORG: number increased each time device sends an initial announce or an update message
    # CONFIGID.UPNP.ORG: number used for caching description information
    # SEARCHPORT.UPNP.ORG: number identifies port on which device responds to unicast M-SEARCH


class Advertisement(SSDPMessage):
    """An SSDP device/service advertisement message."""
    START_LINE = 'NOTIFY * HTTP/1.1'
    
    def __init__(self):
        super(Advertisement, self).__init__()

    def _defaults(self):
        return {} # TODO

    # TODO
    # NOTIFY * HTTP/1.1
    # HOST: 239.255.255.250:1900
    # CACHE-CONTROL: max-age = seconds until advertisement expires
    # LOCATION: URL for UPnP description for root device
    # NT: notification type
    # NTS: ssdp:alive
    # SERVER: OS/version UPnP/1.1 product/version
    # USN: composite identifier for the advertisement
    # BOOTID.UPNP.ORG: number increased each time device sends an initial announce or an update message
    # CONFIGID.UPNP.ORG: number used for caching description information
    # SEARCHPORT.UPNP.ORG: number identifies port on which device responds to unicast M-SEARCH


MESSAGE_TYPES = { SearchRequest.START_LINE: SearchRequest,
        SearchResponse.START_LINE: SearchResponse,
        Advertisement.START_LINE: Advertisement }


class ParsingError(Exception):
    """An SSDP message could not be parsed."""
    pass

class IllegalValueError(Exception):
    """Protocol-disobedience thwarted."""
    pass


def _propname(header):
    return header.lower().replace('-', '_')

def _drop_empty_values(dict_):
    return dict((k, v) for k, v in dict_.items() if v.strip())

def _items_sorted_by_key(dict_):
    return sorted(((k, v) for k, v in dict_.items()))

