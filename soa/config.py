'''
soa.config
~~~~~~~~~~

    Basic configs for SOA.
'''

import os
import logging

# base dir of user's project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# debug
DEBUG = True

# address
ADDRESS = ('127.0.0.1', 8888)

# is web framework, default is web, False means that is a tcp framework
WEB = True


# debug for log filter
class DebugTure(logging.Filter):
    #override
    def filter(self, record):
        return DEBUG
