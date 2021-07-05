'''
    out - Simple logging with a few fun features.
    © 2018-19, Mike Miller - Released under the LGPL, version 3+.
'''
import sys
import out


def test_levels(full=True):

    out('no explicit level, should be info.')
    out.trace('trace msg: %s', 'Absurdly voluminous details…')
    out.debug('debug message')
    out.info('info message - Normal feedback')
    out.note('note message - Important positive feedback to remember.')
    out.warn('warn message - Something to worry about.')

    if full:
        out.critical('critical message - *flatline*')
        out.fatal('fatal message - *flatline*')
        try:
            1/0
        except Exception:
            out.error('error message - Pow!')
            #~ out.exception('exception message - Kerblooey!')
            out.exc('exc message - Kerblooey!')


out.warn('begin...')
print('⏵⏵ print std config:')
out.configure(
    level='trace',   # needs to go before to allow console log to be viewed!
)
out.log_config()
print('---------------------------------')


print('⏵⏵ change to stdout:')
out.configure(
    #~ theme='interactive',
    stream=sys.stdout,  # runs console.detection again
)
out.log_config()
print('---------------------------------')


print('⏵⏵ log messages from module:')
from out import test_mod; test_mod  # pyflakes
print()

print('⏵⏵ test levels:')
test_levels()
print('---------------------------------')


print('⏵⏵ test different highlighting, lexers:')
out.configure(lexer='json')
out.debug('debug message: JSON: %s', '{"data": [null, true, false, "hi", 123]}')

out.configure(lexer='xml')
out.trace('trace message: XML: %s', '<xml><tag attr="woot">text</tag></xml><!-- hi -->')

out.configure(lexer='python3')
out.note('debug message: PyON: %s # hi',
         {'data': [None, True, False, 'hi', 123]})
#~ # out.note('debug message2: PyON: %(data)s # hi',
         #~ # {'data': [None, True, False, 'hi', 123]})
out.note('import foo; [ x for x in y ]')
print('---------------------------------')


print('⏵⏵ test json formatter:')
out.configure(
    level='info',
    # theme='plain',
    theme='json',
)
out('no explicit level')
out.warn('warn: Heavens to Mergatroyd!')
