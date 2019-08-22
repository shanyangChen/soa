'''
soa.web.handler
~~~~~~~~~~~~~~~

    Web.handler's work is to translate data as http data.
    
'''

class Container():

    '''
        When Soa was created, the server soa has binded to this server.
        For see this property evidently, so Marked it there.
    '''
    server = None

    def __call__(self, data):
        self.server.logger.debug("web received data as {}".format(data))
        return bytes('ok ! web received data from soa is {}'.format(data), 'utf-8')

