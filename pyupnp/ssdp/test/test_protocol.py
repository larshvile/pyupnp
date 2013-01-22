import unittest

from pyupnp.ssdp.protocol import *

MSEARCH = 'M-SEARCH * HTTP/1.1'
_200OK = 'HTTP/1.1 200 OK'
NOTIFY = 'NOTIFY * HTTP/1.1'

class ProtocolTest(unittest.TestCase):

    def test_MSEARCH_message_yields_search_request(self):
        msg = read_ssdp_message(self.some_message(MSEARCH))
        self.assertIsInstance(msg, SearchRequest)

    def test_200OK_message_yields_search_reponse(self):
        msg = read_ssdp_message(self.some_message(_200OK))
        self.assertIsInstance(msg, SearchResponse)

    def test_NOTIFY_message_yields_advertisement(self):
        msg = read_ssdp_message(self.some_message(NOTIFY))
        self.assertIsInstance(msg, Advertisement)

    def test_other_messages_cannot_be_read(self):
        with self.assertRaises(ParsingError):
            read_ssdp_message(self.some_message('something else'))
    

    def some_message(self, startline):
        return "%s\r\nHeader: value\r\n" % startline

