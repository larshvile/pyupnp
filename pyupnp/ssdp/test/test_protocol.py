import unittest

from pyupnp.ssdp.protocol import *

MSEARCH = 'M-SEARCH * HTTP/1.1'
_200OK = 'HTTP/1.1 200 OK'
NOTIFY = 'NOTIFY * HTTP/1.1'

class ProtocolTest(unittest.TestCase):

    def test_MSEARCH_message_yields_search_request(self):
        msg = read_ssdp_message(some_msg(MSEARCH))
        self.assertIsInstance(msg, SearchRequest)

    def test_200OK_message_yields_search_reponse(self):
        msg = read_ssdp_message(some_msg(_200OK))
        self.assertIsInstance(msg, SearchResponse)

    def test_NOTIFY_message_yields_advertisement(self):
        msg = read_ssdp_message(some_msg(NOTIFY))
        self.assertIsInstance(msg, Advertisement)

    def test_other_messages_cannot_be_read(self):
        with self.assertRaises(ParsingError):
            read_ssdp_message(some_msg('something else'))

    def test_headers_are_persisted_in_parsed_message(self):
        msg = read_ssdp_message(msg_with_headers(K1 = 'a', K2 = 'b'))
        self.assertEqual('a', msg.headers['K1'])
        self.assertEqual('b', msg.headers['K2'])

    def test_header_keys_are_stored_in_upper_case(self):
        msg = read_ssdp_message(msg_with_headers(key = 'value'))
        self.assertIn('KEY', msg.headers)

    def test_header_values_are_stripped_for_whitespace(self):
        msg = read_ssdp_message(msg_with_headers(key = '  value  '))
        self.assertEqual('value', msg.headers['KEY'])
 

def some_msg(startline, **headers):
    hdstr = ['%s: %s' % (k, v) for k, v in headers.items()]
    return "%s\r\n%s\r\n" % (startline, '\r\n'.join(hdstr))

def msg_with_headers(**headers):
    return some_msg(MSEARCH, **headers)

