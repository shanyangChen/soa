'''
soa.web.errhandler
~~~~~~~~~~~~~~~~~~

    The handler includes such many codes and means.
    For example as 302,303.../400,402,403,404../500..
'''

class ErrHandler:

    def __init__(self, code, status):
        self.template = '''
            <html>
            <body>
            {!r}
            <hr>

            <h5>SOA, a rest time framework. learning and by learning ( ~ .~)</h5>
            </body>
            </html>
        '''
        self.code = code
        self.status = status

    def translate(self):
        return self.template.format(self.status)
        

class Error400(ErrHandler):
    def __init__(self):
        super().__init__(400, 'Bad Request')

class Error401(ErrHandler):
    def __init__(self):
        super().__init__(401, 'Unauthorized')

class Error402(ErrHandler):
    def __init__(self):
        self.code = 402
        super().__init__(402, 'Payment Required')

class Error403(ErrHandler):
    def __init__(self):
        super().__init__(403, 'Forbidden')

class Error404(ErrHandler):
    def __init__(self):
        super().__init__(404, 'Not Found')

class Error405(ErrHandler):
    def __init__(self):
        self.code = 405
        super().__init__(405, 'Method Not Allowed')

class Error406(ErrHandler):
    def __init__(self):
        super().__init__(406, 'Not Acceptable')

class Error407(ErrHandler):
    def __init__(self):
        super().__init__(407, 'Proxy Authentication Required')

class Error408(ErrHandler):
    def __init__(self):
        super().__init__(408, 'Request Timeout')

class Error409(ErrHandler):
    def __init__(self):
        super().__init__(409, 'Conflict')

class Error500(ErrHandler):
    def __init__(self):
        super().__init__(500, 'Internal Server Error')

class Error501(ErrHandler):
    def __init__(self):
        super().__init__(501, 'Not Implemented')

class Error502(ErrHandler):
    def __init__(self):
        super().__init__(502, 'Bad Gateway')

class Error503(ErrHandler):
    def __init__(self):
        super().__init__(503, 'Service Unavailable')

class Error504(ErrHandler):
    def __init__(self):
        super().__init__(504, 'Gateway Timeout')

class Error505(ErrHandler):
    def __init__(self):
        super().__init__(505, 'HTTP Version Not Supported')

class Error506(ErrHandler):
    def __init__(self):
        super().__init__(506, 'Variant Also Negotiates')

class Error507(ErrHandler):
    def __init__(self):
        super().__init__(507, 'Insufficient Storage')

class Error508(ErrHandler):
    def __init__(self):
        super().__init__(508, 'Loop Detected')

class Error510(ErrHandler):
    def __init__(self):
        super().__init__(510, 'Not Extended')

class Error511(ErrHandler):
    def __init__(self):
        super().__init__(511, 'Network Authentication Required')
