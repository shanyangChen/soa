'''
soa.exceptions
~~~~~~~~~~~~~~
    It contains some exceptions for this framework,
    it's a normal way to deal with exceptions, so I
    do it.
'''

# basic exception of soa
class SoaException(Exception):
    '''
        :message: the error message of exception, custom.
        :code: it provides a way to send signal to client(HTTP or somes)
    '''
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

# container
class NotContainer(SoaException):
    pass

# Router
class URIConflictsException(SoaException):
    pass

class RouterLostFuncException(SoaException):
    pass

class URINotRegistered(SoaException):
    pass

# Header
class NotDictHeaders(SoaException):
    pass
