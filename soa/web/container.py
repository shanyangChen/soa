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
from soa.web import errhandler

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
        self.req_middleawres = config.REQ_MIDDLEWARES
        self.res_middleawres = config.RES_MIDDLEWARES
        self.client_listeners = {}  # peername : request

    def __call__(self, data, remote_addr):
        # hand it to request
        ip, port = remote_addr
        ra = ip + ':' + str(port)
        if self.client_listeners.get(ra):
            request = self.client_listeners[ra]
        else:
            request = self.requester(self.server, remote_addr)
            self.client_listeners[ra] = request
        # feed data for request
        request.catch_data(data)

        # handle request middlewares #
        request = self.middlewares_handle(self.req_middleawres, request)

        handler = self.router.get_func_by_uri(request.path, request.method)
        if not handler:
            # 404
            err = errhandler.Error404()
            request.set_headers({'Content-Type':'text/html;charset=utf-8'})
            response = self.responser(err.translate(), False, host=request.host, headers=request.user_headers, keep_alive_time_rest=request.keep_alive_time_rest)
        else:
            result = handler(request)   # we hope that the handler will be run as a croutine later

            # handle response middlewares #
            result = self.middlewares_handle(self.res_middleawres, response)

            response = self.responser(result, request.is_json, host=request.host, headers=request.user_headers, keep_alive_time_rest=request.keep_alive_time_rest)

            # check keep_alive timeout
            if self.check_kp_timeout(request):
                del self.client_listeners[request.remote_addr]

        return response.build_bytes()

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

    def middlewares_handle(self, middlewares, obj):
        for ware in middlewares:
            # It means that ware is the Class of middleware
            obj = ware(obj)
        return obj
    
    def check_kp_timeout(self, request):
        return request.keep_alive_time_rest <= 0
        

