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
    startline, *headers = msg_string.splitlines()
    msgtype = MESSAGE_TYPES.get(startline)
    if msgtype is None:
        raise ParsingError('Invalid SSDP start-line "%s"' % startline)
    return msgtype(headers)


class SSDPMessage: # TODO does this even make sense?
    # TODO common headers?, nope.. Though Advertisement & SearchResponse shares some
    pass
    # TODO pack(recipient) : str ?


class SearchRequest(SSDPMessage):
    """An SSDP search request, issued to locate devices and services."""
    START_LINE = 'M-SEARCH * HTTP/1.1'

    def __init__(self, headers):
        pass

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


MESSAGE_TYPES = { SearchRequest.START_LINE: SearchRequest,
        SearchResponse.START_LINE: SearchResponse,
        Advertisement.START_LINE: Advertisement }


class ParsingError(Exception):
    """Signals that an SSDP message could not be parsed."""
    pass

