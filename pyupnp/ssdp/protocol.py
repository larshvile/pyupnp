# TODO module docs please


class ParsingError(Exception):
    # TODO doc / improve
    pass


def read_ssdp_message(msg_string):
    # TODO docme
    startline, *headers = msg_string.splitlines()
    msgtype = MESSAGE_TYPES.get(startline)
    if msgtype is None:
        raise ParsingError('Invalid SSDP start-line "%s"' % startline)
    return msgtype(headers)


class SSDPMessage: # TODO does this even make sense?
    # TODO common headers?, nope.. Though Advertisement & SearchResponse shares some
    pass
    # TODO pack(recipient) : str ?
    # TODO unpack(str)? - a factory should probably be doing that..


class SearchRequest(SSDPMessage):
    # TODO docme
    START_LINE = 'M-SEARCH * HTTP/1.1'
    def __init__(self, headers):
        pass


class SearchResponse(SSDPMessage):
    # TODO docme
    START_LINE = 'HTTP/1.1 200 OK'
    def __init__(self, headers):
        pass


class Advertisement(SSDPMessage):
    # TODO docme
    START_LINE = 'NOTIFY * HTTP/1.1'
    def __init__(self, headers):
        pass


MESSAGE_TYPES = { SearchRequest.START_LINE: SearchRequest,
        SearchResponse.START_LINE: SearchResponse,
        Advertisement.START_LINE: Advertisement }

