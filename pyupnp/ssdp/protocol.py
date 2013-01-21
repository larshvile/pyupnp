# TODO module docs please

import platform


# TODO rampant prefixing galore..?


class ParsingError(Exception):
    # TODO doc / improve
    pass


def parse_ssdp_message(msg):
    # TODO docme
    start, *headers = msg.splitlines()
    # TODO if??
    if (start == 'M-SEARCH * HTTP/1.1'):
        return SearchRequest(headers)
    elif (start == 'HTTP/1.1 200 OK'):
        return SearchResponse(headers)
    elif (start == 'NOTIFY * HTTP/1.1'):
        return Advertisement(headers)
    else:
        raise ParsingError('Invalid SSDP start-line "%s"' % start)


class SSDPMessage: # TODO does this even make sense?
    # TODO common headers?
    pass
    # TODO pack(recipient) : str ?
    # TODO unpack(str)? - a factory should probably be doing that..


class SearchRequest(SSDPMessage):
    # TODO docme
    def __init__(self, headers):
        pass


class SearchResponse(SSDPMessage):
    # TODO docme
    def __init__(self, headers):
        pass


class Advertisement(SSDPMessage):
    # TODO docme
    def __init__(self, headers):
        pass



# class SSDPAdvertisement


# TODO please replace this crud with proper unit tests
if __name__ == '__main__':
    print('Testing')

