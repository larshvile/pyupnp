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
        for (k, v) in headers.items():
            prop = cls._propname(k)
            if hasattr(msg, prop):
                setattr(msg, prop, v)
            else:
                msg.headers[k] = v
        return msg

    @staticmethod
    def _propname(header):
        return header.lower().replace('-', '_')

    def __init__(self):
        self.headers = {}

    def __repr__(self):
        hdr_with_val = dict((k, v) for k, v in self.headers.items() if v)
        return self.__class__.__name__ + ' ' + pformat(hdr_with_val)

    # TODO transform to msg string for transport


class SearchRequest(SSDPMessage):
    """An SSDP search request, issued to locate devices and services."""
    START_LINE = 'M-SEARCH * HTTP/1.1'

    def __init__(self):
        super(SearchRequest, self).__init__()

    @property
    def key(self):
        return self.headers.get('KEY')

    @key.setter
    def key(self, value):
        # TODO validate, parse_headers could convert to parsing err
        self.headers['KEY'] = value
    
    # TODO host/port should be set as late as possible, ideally during transfer..
        # - alternatively it could default to multicast, and be used as the actual
        # address during transfer

    # HOST: 239.255.255.250:1900 => based on host
    # MAN: "ssdp:discover" => constant
    # MX: seconds to delay response => must be >=1, should be <=5
    # ST: search target
    # USER-AGENT: OS/version UPnP/1.1 product/version


class SearchResponse(SSDPMessage):
    """The response to an SSDP search request."""
    START_LINE = 'HTTP/1.1 200 OK'

    def __init__(self):
        super(SearchResponse, self).__init__()

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
    """Signals that an SSDP message could not be parsed."""
    pass

