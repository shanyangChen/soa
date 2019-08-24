'''
soa.web.router
~~~~~~~~~~~~~~

    Router is designed to analyse Request for web server resources.
    The most important meterial is URI, and as a web server, `GET`
    should be a ordinary method to request server resource. And it
    Maybe a file as stream, so, It should be designed to handle 
    stream. Let's do it!
'''

import uuid

from soa import exceptions

class Router:
    
    '''
        Too many web framework likes to design the route as a `@` which
        can mark upon on callable functions to deal with different requests.
        It seems easyer, like flask, sanic and so on. And the framewok
        also provides registion way to handle request. django's way of Router
        is configuarte by urls.py(`urlpatterns=[url(r'^hello/soa$', views.hello),]`).
        Think about some web framework as we learn, maybe it not important 
        to choose a way, most importantly, it is effective.

        Then we just manage every url of function handler.
    '''

    def __init__(self):
        '''
            :uri_funcs: cache the uri-function as k-v to handle request as GET/POST etc.
        '''
        # keep it later for dynamic router access
        # if dynamic router is ok, we could use lru_cache to cache the router
        # for router uri. also, for more convenient, it will add manage dynamic
        # functions for Router.
        self.pattern = {
            'str' : (str, r'[^/]+'),       
            'int' : (int, r'[0-9]+'),
            'path': (str, r'[^/].*'),
            'normal':(str,r'[a-zA-Z0-9_-]+'),
            'uuid': (uuid.UUID, r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
        }
        self.uri_funcs = {}

    def add(self, original_uri, func, method):
        uri = self.parser(original_uri)
        if not uri:
            raise URIConflictsException(
                    'The router uri is conflicts, please set it as `/module/controller/function`'   
                )
        if not func:
            raise RouterLostFuncException(
                    'The router uris has not provided func for uri.'   
                )
        self.uri_funcs[uri] = (method, func)

    def get_func_by_uri(self, uri, method):
        # it will return 404 response for request
        if self.uri_funcs.get(uri):
            t = self.uri_funcs[uri]  
            if t[0].issubset(method.upper()):
                return t[1]
        return None

    def parser(self, original_uri):
        # maybe it will effective for soa.web framework, we will update it when it is necessary
        return original_uri
