from nose.tools import *
from pyupnp.ssdp.protocol import *

MSEARCH = 'M-SEARCH * HTTP/1.1'
_200OK = 'HTTP/1.1 200 OK'
NOTIFY = 'NOTIFY * HTTP/1.1'

class TestProtocol:

    def test_MSEARCH_message_yields_search_request(self):
        msg = parse_ssdp_message(msg_string(MSEARCH))
        assert type(msg) == SearchRequest

    def test_200OK_message_yields_search_reponse(self):
        msg = parse_ssdp_message(msg_string(_200OK))
        assert type(msg) == SearchResponse

    def test_NOTIFY_message_yields_advertisement(self):
        msg = parse_ssdp_message(msg_string(NOTIFY))
        assert type(msg) == Advertisement

    @raises(ParsingError)
    def test_other_messages_cannot_be_read(self):
        parse_ssdp_message(msg_string('something else'))

    def test_headers_are_persisted_in_parsed_message(self):
        msg = parse_ssdp_message(msg_string(K1 = 'a', K2 = 'b'))
        assert msg._headers['K1'] == 'a'
        assert msg._headers['K2'] == 'b'

    def test_header_keys_are_stored_in_upper_case(self):
        msg = parse_ssdp_message(msg_string(key = 'v'))
        assert 'KEY' in msg._headers

    def test_header_values_are_stripped_for_whitespace(self):
        msg = parse_ssdp_message(msg_string(key = ' v '))
        assert msg._headers['KEY'] == 'v'

    def test_parsed_message_does_not_contain_empty_header(self):
        msg = parse_ssdp_message(msg_string())
        assert '' not in msg._headers

    def test_header_keys_are_converted_to_uppercase(self):
        msg = some_message()
        msg.set_headers(test = 'some')
        assert 'TEST' in msg._headers

    def test_headers_in_encoded_message_are_sorted_alphabetically(self):
        msg = some_message()
        msg.set_headers(x = 'some', y = 'other')
        assert 'X: some\r\nY: other' in msg.encode()

    def test_encoded_message_is_identical_to_the_original(self):
        orig = 'M-SEARCH * HTTP/1.1\r\n'\
               'HOST: host:port\r\n'\
               'MAN: "ssdp:discover"\r\n'\
               'MX: 1\r\n'\
               'ST: ssdp:all\r\n'\
               'USER-AGENT: agentX\r\n'
        assert parse_ssdp_message(orig).encode() == orig

    def test_empty_headers_are_excluded_from_repr_output(self):
        msg = parse_ssdp_message(msg_string(h1 = '1', h2 = ''))
        assert 'H1' in repr(msg)
        assert 'H2' not in repr(msg)

    def test_fresh_message_is_initialized_with_default_values(self):
        msg = SearchRequest()
        assert 'MX' in msg._headers

    def test_default_values_are_not_present_in_parsed_messages(self):
        msg = SearchRequest.from_headers({'a': 'b'})
        assert 'MX' not in msg._headers
        assert 'A' in msg._headers


def msg_string(startline = MSEARCH, **headers):
    hdrs = ['%s: %s' % (k, v) for k, v in headers.items()]
    return "%s\r\n%s\r\n" % (startline, '\r\n'.join(hdrs))

def some_message():
    return SearchRequest()

