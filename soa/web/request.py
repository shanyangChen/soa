'''
soa.web.request
~~~~~~~~~~~~~~~

    Requester will analys the request of client, maybe some job
    of this analysis is awaitable so we can change the execution flow
    as a coroutine by others.
'''

from weakref import proxy
import re
from urllib.parse import unquote, urlparse 
from collections import defaultdict
from time import time

from soa.web import config
from soa.exceptions import NotDictHeaders

class Requester:

    '''
        The object of Requester will be a paramter of reuqest handler,
        when request parse b-data as header/body and uri, then catch
        the handler by router, and put the request object as paramter
        in the handler, to provide body for this handler. The brige of
        this job flow is container as server, the container will catch
        the return value by handler when handler return, then container
        call response object to wrap the return value as body, provides
        complete response for client which includes header,body,some 
        rules of current C/S communication and so on.
    '''
    # default content-type
    #DEFAULT_CONTENT_TYPE = 'application/octect-stream'

    def __init__(self, server, remote_addr):
        self.remote_addr = remote_addr
        self.server = proxy(server)
        self.headers = defaultdict(list)
        self.body = []
        self.host = ''
        self.url = ''
        self.scheme = ''
        self.netloc = ''
        self.path = ''
        self.method = ''
        self.query = {}
        self.files = {}
        self.form = {}
        self.POST = {}
        self.GET = {}
        self.cookies = {}
        self.version = None
        self.is_json = False                    # when translate data by json please set it true
        self.keep_alive = config.KEEP_ALIVE     # 0:closed >0: keep_alive_time
        self.keep_alive_time = time()*1000      # base ms
        self.user_headers = {}


    def catch_data(self, b_data):
        # update keep_alive
        self.keep_alive_time_rest = int(self.keep_alive-(time()*1000 - self.keep_alive_time))

        self.data = bytes.decode(b_data, 'latin-1')    # defaut is latin-1(iso-8859-1)
        parts = self.data.split('\r\n\r\n')
        main = parts.pop(0)
        main_parts = main.split('\r\n')
        title = main_parts.pop(0)
        self.method, url, self.version = title.split(' ')
        # unquote the ascii url to utf-8
        self.url = unquote(url)
        for s in main_parts:
            h_name, h_value = s.split(':', 1)
            if h_name.strip().upper() == 'HOST':
                self.host = h_value
            if h_name.strip().upper() == 'COOKIE':
                cookies = SimpleCookie()
                cookies.load(h_value)
                self.cookies = { name: cookie.value for name, cookie in cookies.items() }
            h_value = h_value.split(',')
            self.headers[h_name.upper()] = h_value

        # catch boundary form Content-Type, it is a form request
        # if the boundary existed.
        boundary = None
        if self.headers['CONTENT-TYPE'] and len(self.headers['CONTENT-TYPE']) > 0:
            cty_str = self.headers['CONTENT-TYPE'][0].split(';')
            content_type = cty_str[0]
            for s in cty_str:
                s = s.strip()
                if s.startswith('boundary='):
                    boundary = s.replace('boundary=', '--')
        
        # parse url
        url_obj = urlparse(self.url)
        self.scheme = url_obj.scheme
        self.netloc = url_obj.netloc
        self.path = url_obj.path
        self.query = self.parse_query(url_obj.query)
        self.GET = self.query

        # parse body
        woo = ''.join(parts)
        is_complete = False
        if boundary:
            # form/data
            body_parts = woo.split(boundary)
            col_query_reg = re.compile(r'name=\"(.*)\"(.*)')
            file_query_reg = re.compile(r'filename="(.*)"')
            for item in body_parts:
                item = item.strip()
                if not item:
                    continue
                if item == '--':
                    is_complete = True
                else:
                    # query[k,v]
                    col_matched = col_query_reg.search(item)
                    ele = col_matched.groups(0) if col_matched else None
                    if ele:
                        qk, qv = ele
                        self.form[qk] = qv
                    # file
                    file_matched = file_query_reg.search(item)
                    ele = file_matched.groups(0) if file_matched else None
                    if ele:
                        fk = ele[0]
                        fv = item.split('\r\n')[-1]
                        self.files[fk] = fv
            self.POST = self.form
        else:
            # row_data
            self.POST = woo

        # TEST:
        #print('GET ------------------------------------------')
        #print(self.GET)
        #print('POST ------------------------------------------')
        #print(self.POST)
        #print('FILE ------------------------------------------')
        #print(self.files)
            

    def parse_query(self, uri):
        '''
            Attention: It is not analys type of value, 
            it would be flexible for value using
            It handles path like `/path?k1=v1&k2=v2`, it does not 
            support `/path/v1/v2`, it will be suppoerted by next
            issue.
        '''
        if uri:
            res = dict()
            parts = uri.split('&')
            for item in parts:
                k, v = item.split('=')
                res[k] = v
            return res
        return ''
    
    def set_json_header(self, is_json=False):
        self.is_json = is_json

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise NotDictHeaders(
                    'The headers param not instance of dict.'   
                )
        self.user_headers = headers
        
