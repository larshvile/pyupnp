import unittest

# TODO figure out exactly how this stuff works..
from pyupnp.ssdp.protocol import *

class ProtocolTest(unittest.TestCase):

    def test_search_request_is_created(self): # TODO naming..?
        msg = parse_ssdp_message(self.some_message('M-SEARCH * HTTP/1.1'))
        self.assertIsInstance(msg, SearchRequest)

    def test_search_response_is_created(self): # TODO naming
        msg = parse_ssdp_message(self.some_message('HTTP/1.1 200 OK'))
        self.assertIsInstance(msg, SearchResponse)

    def test_advertisement_is_created(self): # TODO naming
        msg = parse_ssdp_message(self.some_message('NOTIFY * HTTP/1.1'))
        self.assertIsInstance(msg, Advertisement)

    def test_other_messages_cannot_be_created(self):
        with self.assertRaises(ParsingError):
            parse_ssdp_message(self.some_message('UNKNOWN START-LINE'))
    

    def some_message(self, startline):
        return "%s\r\nHeader: value\r\n" % startline

