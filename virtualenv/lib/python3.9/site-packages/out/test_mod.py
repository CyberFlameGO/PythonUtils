'''
    Demo of standard module logging.

'''

import logging

log = logging.getLogger(__name__)


log.debug('debug text from module')
log.info('info text from module')
log.note('note text from module')
log.warn('warning text from module')
log.fatal('fatal text from module')
