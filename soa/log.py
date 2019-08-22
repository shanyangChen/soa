'''
soa.log
~~~~~~~~~~~

    soa.log's config.
    .. code :: python
        import log
        
        logger = log.getLogger('soa')
        logger.console('test one')
        logger.info('test one')
        logger.error('test one')
'''

import logging.config
import os
import time

import config

LOG_DIR = os.path.join(config.BASE_DIR, 'log')
LOG_DIR_INFO = os.path.join(LOG_DIR,'info')
LOG_DIR_ERROR = os.path.join(LOG_DIR,'err')
if not os.path.exists(LOG_DIR): os.mkdir(LOG_DIR)
if not os.path.exists(LOG_DIR_INFO): os.mkdir(LOG_DIR_INFO)
if not os.path.exists(LOG_DIR_ERROR): os.mkdir(LOG_DIR_ERROR)


CONFIG_DEFAULT = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'formatters' : {
        'simple' : {
            'format' : '%(levelname)s [%(asctime)s] [%(filename)s] %(message)s',
        },   
        # 还没有接入请求 这里没有可格式化的host request 等参数
        #'verbose' : {
        #    'format' : '%(levelname)s [%(asctime)s] [%(filename)s] [%(host)s] - ' \
        #    '%(request)s %(message)s %(status)d %(byte)d',
        #},
    },

    # the log recorder filter needs the callable func as return but ture or false
    # the DebugTure is a class extends logging.Filter and provides filter func
    'filters' : {
        'debug_filter' : {
            '()' : 'config.DebugTure',  
        }   
    },

    'handlers' : {
        'console' : {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple',
            'filters' : ['debug_filter'],
        },
        'access' : {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',   
            'filename' : os.path.join(LOG_DIR_INFO,'{}.log'.format(time.strftime('%Y-%m-%d_%H'))),
            'maxBytes' : 10 * 1024 * 1024,
            'backupCount' : 50,
            'formatter' : 'simple',
            'encoding' : 'utf-8',
        },
        'err' : {
            'level' : 'ERROR',
            'class' : 'logging.handlers.RotatingFileHandler',   
            'filename' : os.path.join(LOG_DIR_ERROR,'{}.log'.format(time.strftime('%Y-%m-%d_%H'))),
            'maxBytes' : 10 * 1024 * 1024,
            'backupCount' : 50,
            'formatter' : 'simple',
            'encoding' : 'utf-8',
        },
    },
    
    'loggers' : {
        'soa' : {
            'handlers' : ['console', 'access', 'err'],
            'level' : 'DEBUG',
            'propagate' : True,
        },       
    },
}

logging.config.dictConfig(CONFIG_DEFAULT)
