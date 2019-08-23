'''
soa.web.request
~~~~~~~~~~~~~~~

    Request will analys the request of client, maybe some job
    of this analysis is awaitable so we can change the execution flow
    as a coroutine by others.
'''

from collections import defaultdict

class Requester:

    '''
        The object of Request will be a paramter of reuqest handler,
        when request parser b-data as header/body and uri, then catch
        the handler by router, and put the request object as paramter
        in the handler, to provide body for this handler. The brige of
        this job flow is container as server, the container will catch
        the return value by handler when handler return, then container
        call response object to wrap the return value as body, provides
        complete response for client which includes header,body,some 
        rules of current C/S communication and so on.
    '''

    DEFAULT_CONTENT_TYPE = 'application/octect-stream'

    def __init__(self, server, b_data):
        self.server = server
        self.data = b_data
        self.headers = defaultdict(list)
        self.body = []
        self.url = ''
        self.path = ''
        self.method = ''
        self.url_args = {}
        self.files = None
        self.form = None
        self.json = None
        self.raw_data = None
        self.cookies = None
