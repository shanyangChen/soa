'''
soa.DTH (data transport handler)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    dth bases on python3.7's asyncio module, deal with data event loop.
    
    It designed as a base tcp stream handler to tansport data with web framework
    or other tcp framework like game. sure, as you see it looks more like a 
    leanrning work, so I wish that you can contribut it by your rest time as me,
    and we can enjoy it with others, learning more, happy more.
'''

from asyncio import Protocol, get_event_loop
from functools import partial
from logging import getLogger

import config
import log
from web import container as web
import exceptions

class Soa:
    '''
        SOA: it contains basic env like a container
            but protocol env is designed into protocol's container like web.
            Every protocol has own container, so that can manager itselfies
            env, DHT just porvides faster way to communicate with client, and
            the protocol should suit to different work as you need.

        :coin: web=Ture, other=Fasle
    '''

    def __init__(self, name=None, coin=True):
        if name is None:
            name = '[hello SOA]'
        if coin:
            container = web.Container()
        else:
            container = None   # keep it for later
        # debug
        if not container:
            raise exceptions.NotContainer(
                    'Soa has no Container for your work! '
                    'Maybe current version just provides '
                    'web container, so is your work real fit the current version ? Good lucky !'
                )

        self.name = name
        self.container = container
        self.logger = getLogger('soa')
        self.config = config
        self.loop = get_event_loop()
        self.container.server = self


    def start(self):
        address = self.config.ADDRESS
        PDTH = partial(DTH, self, self.logger)
        factory = self.loop.create_server(PDTH, *address)
        try:
            self.logger.info('Hello SOA ~')
            server = self.loop.run_until_complete(factory)
            self.loop.run_forever()
        finally:
            server.close()
            self.loop.run_until_complete(server.wait_closed())
            self.loop.close()
            self.logger.info('SOA is stopped, GoodBye ~')
            quit()
        

class DTH(Protocol):
    '''
        DTH: Data Transport Handler
        override methods from asyncio.Protocol, data_received,
        connection_made, connection_lost
    '''

    def __init__(self, server, logger):
        self.server = server
        self.logger = logger

    def connection_made(self, transport):
        self.transport = transport
        self.client_addr = transport.get_extra_info('peername')

    def data_received(self, data):
        response = self.server.container(data, self.client_addr)
        self.transport.write(response)

        # debug
        self.logger.debug('[received bytes]-------------------------------------------')
        self.logger.debug(data)
        self.logger.debug('[send bytes]-----------------------------------------------')
        self.logger.debug(response)

    def connection_lost(self, exc):
        if exc:
            self.logger.error('{}.{} disconnected err: exc: {!r}.'.format(*self.client_addr, exc))
        self.logger.info('{}.{} disconnected.'.format(*self.client_addr))
        super().connection_lost(exc)
                
