"""
# TODO, PEP 257 sez..
The docstring for a module should generally list the classes, exceptions
and functions (and any other objects) that are exported by the module,
with a one-line summary of each. (These summaries generally give less detail
than the summary line in the object's docstring.) The docstring for a package
(i.e., the docstring of the package's __init__.py module) should also
list the modules and subpackages exported by the package.
"""


def read_ssdp_message(msg_string):
    """Parse an SSDP message provided as text."""
    start_line, *header_lines = msg_string.splitlines()
    
    msgtype = MESSAGE_TYPES.get(start_line)
    if msgtype is None:
        raise ParsingError('Invalid SSDP start-line "%s"' % start_line)
  
    header_kvs = [(k.upper(), v.strip()) for (k, s, v) in
            [l.partition(':') for l in header_lines]]

    return msgtype(dict(header_kvs))


# TODO toString / repr stuff?
class SSDPMessage: # TODO does this even make sense?
    # TODO common headers?, nope.. Though Advertisement & SearchResponse shares some
    pass


class SearchRequest(SSDPMessage):
    """An SSDP search request, issued to locate devices and services."""
    START_LINE = 'M-SEARCH * HTTP/1.1'

    def __init__(self, headers):
        self.headers = headers # TODO need to do better than this =)
        pass

    # TODO host/port should be set as late as possible, ideally during transfer..
    # maybe this can be solved by having an abstract setHost() in SSDPMessage?
    # the transport infrastructure could invoke this before serializing the msg

    # HOST: 239.255.255.250:1900 => based on host
    # MAN: "ssdp:discover" => constant
    # MX: seconds to delay response => must be >=1, should be <=5
    # ST: search target
    # USER-AGENT: OS/version UPnP/1.1 product/version


class SearchResponse(SSDPMessage):
    """The response to an SSDP search request."""
    START_LINE = 'HTTP/1.1 200 OK'

    def __init__(self, headers):
        pass


class Advertisement(SSDPMessage):
    """An SSDP device/service advertisement message."""
    START_LINE = 'NOTIFY * HTTP/1.1'
    
    def __init__(self, headers):
        pass

    # TODO HOST .. same as SearchRequest, but this one is actually constant??


MESSAGE_TYPES = { SearchRequest.START_LINE: SearchRequest,
        SearchResponse.START_LINE: SearchResponse,
        Advertisement.START_LINE: Advertisement }


class ParsingError(Exception):
    """Signals that an SSDP message could not be parsed."""
    pass

