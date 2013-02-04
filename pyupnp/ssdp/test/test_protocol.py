import unittest

from pyupnp.ssdp.protocol import *

MSEARCH = 'M-SEARCH * HTTP/1.1'
_200OK = 'HTTP/1.1 200 OK'
NOTIFY = 'NOTIFY * HTTP/1.1'

class ProtocolTest(unittest.TestCase):

    def test_MSEARCH_message_yields_search_request(self):
        msg = parse_ssdp_message(msg_string(MSEARCH))
        self.assertIsInstance(msg, SearchRequest)

    def test_200OK_message_yields_search_reponse(self):
        msg = parse_ssdp_message(msg_string(_200OK))
        self.assertIsInstance(msg, SearchResponse)

    def test_NOTIFY_message_yields_advertisement(self):
        msg = parse_ssdp_message(msg_string(NOTIFY))
        self.assertIsInstance(msg, Advertisement)

    def test_other_messages_cannot_be_read(self):
        with self.assertRaises(ParsingError):
            parse_ssdp_message(msg_string('something else'))

    def test_headers_are_persisted_in_parsed_message(self):
        msg = parse_ssdp_message(msg_string(K1 = 'a', K2 = 'b'))
        self.assertEqual('a', msg.headers['K1'])
        self.assertEqual('b', msg.headers['K2'])

    def test_header_keys_are_stored_in_upper_case(self):
        msg = parse_ssdp_message(msg_string(key = 'v'))
        self.assertIn('KEY', msg.headers)

    def test_header_values_are_stripped_for_whitespace(self):
        msg = parse_ssdp_message(msg_string(key = ' v '))
        self.assertEqual('v', msg.headers['KEY'])

    def test_parsed_message_does_not_contain_empty_header(self):
        msg = parse_ssdp_message(msg_string())
        self.assertNotIn('', msg.headers)
 

def msg_string(startline = MSEARCH, **headers):
    hdstr = ['%s: %s' % (k, v) for k, v in headers.items()]
    return "%s\r\n%s\r\n" % (startline, '\r\n'.join(hdstr))

