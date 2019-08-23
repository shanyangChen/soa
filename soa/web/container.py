'''
soa.web.container
~~~~~~~~~~~~~~~~~

    Web.container's work is to translate data as http data.
    And it has HTTP basic environment, so let's do it !
    
'''

from soa.web import router
from soa.web import request
from soa.web import response
from soa.web import config

class Container():

    '''
        When Soa was created, the server soa has binded to this server.
        For see this property evidently, so Marked it there.
    '''
    server = None

    def __init__(self):
        self.router = router.Router()
        self.requester =  request.Requester
        self.responser = response.Responser
        self.middleawres = config.MIDDLEWARES

    def __call__(self, data):
        # hand it to request
        request = self.requester(self.server, data)
        return bytes('ok ! web received data from soa is {}'.format(data), 'utf-8')

    def route(self, uri, method=frozenset({'GET'})):
        '''
            It designed as a wrap for router handlers.
            It could be a sub zone as get / post .. methods.
        '''
        uri = uri.strip()
        if uri[0] != '/': uri = '/' + uri
        
        # wrapped
        def map_uri(handler):
            self.router.add(uri, handler, method)
            return map_uri
        return map_uri
    
    def get(self, uri, method=frozenset({'GET'})):
        return self.route(uri, method)
        
    def post(self, uri, method=frozenset({'POST'})):
        return self.route(uri, method)

    def head(self, uri, method=frozenset({'HEAD'})):
        return self.route(uri, method)

    def put(self, uri, method=frozenset({'PUT'})):
        return self.route(uri, method)
    # remove trace/options/patch/delete/connection methods.

