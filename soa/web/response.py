'''
soa.web.response
~~~~~~~~~~~~~~~~

    Responser will package the data as d the http message.
    Title
    -----------------
    Headers

    ----------------
    Body
'''

from datetime import datetime
import json

GMT = '%a, %d %b %Y %H:%M:%S GMT'
DEFAULT_RESPONSE_STRUCT = '' \
'HTTP/{!s} {!s} {!s}\r\n' \
'{!s}' \
'\r\n' \
'{!s}' \
'\r\n'

class Responser:

    def __init__(self, data, is_json, version='1.1', host=None, headers={}, keep_alive_time_rest=False):
        '''
            Attention: we should base on request condition to contribute response,
            So a sensible way is that let user build headers too if needed.
            And the responser has own basic headers for text/plain, and status code.
        '''
        self.version = version
        self.code = 200
        self.status = 'OK'
        self.host = host
        self.content_type = 'application/json; charset=utf-8' if is_json else 'text/plain; charset=utf-8' 
        self.connection = 'keep-alive' if keep_alive_time_rest else 'closed'
        self.keep_alive_time_rest = str(int(keep_alive_time_rest/1000))+'s' if keep_alive_time_rest > 1000 else str(keep_alive_time_rest)+'ms'
        self.headers = {}
        self.body = data
        self.user_headers = headers
        
    def build_bytes(self):
        # build headers
        self.headers['Content-Type'] = self.content_type
        self.headers['Connection'] = self.connection
        self.headers['Keep-Alive'] = self.keep_alive_time_rest if self.keep_alive_time_rest else None   # should I put the config value?
        self.headers['Date'] = datetime.now().strftime(GMT)
        self.headers['Server'] = self.host
        self.headers['Content-Length'] = len(self.body)  # bytes len == str len (as utf-8)
        # merge_headers, b will cover a if same key
        headers = {**self.headers, **self.user_headers}
                
        woo_headers = ''
        for k,v in headers.items():
            woo_headers += '{}:{}\r\n'.format(k,v)

        # build body
        if self.content_type == 'application/json' and self.body:
            data = json.loads(self.body)
            if data.code != 200:
                self.code = data.code
            if data.status:
                self.status = data.status
        
        # parse to bytes response_struct
        response = DEFAULT_RESPONSE_STRUCT.format(
                self.version,
                self.code,
                self.status,
                woo_headers,
                self.body
            )
        return bytes(response, 'latin-1')   # it should be encode by content-type`s charset
        
