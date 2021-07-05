'''
    out - Simple logging with a few fun features.
    © 2018-2020, Mike Miller - Released under the LGPL, version 3+.
'''
import os
import sys
import logging
import traceback

from .detection import _find_palettes, is_fbterm


# detect environment before loading formatters and themes
_out_file = sys.stderr
fg, bg, fx, _level, _is_a_tty  = _find_palettes(_out_file)


# now we're ready to import these:
from .format import (ColorFormatter as _ColorFormatter,
                     JSONFormatter as _JSONFormatter)
from .themes import (render_themes as _render_themes,
                     render_styles as _render_styles,
                     icons as _icons)

__version__ = '0.78'

# Allow string as well as constant access.  Levels will be added below:
level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'warning': logging.WARN,
    'err': logging.ERROR,
    'error': logging.ERROR,
    'critical': logging.FATAL,
    'fatal': logging.FATAL,
}


class Logger(logging.Logger):
    '''
        A singleton logger with centralized configuration.
    '''
    default_level = logging.INFO
    __path__ = __path__         # allows python3 -m out.demos to work
    __version__ = __version__
    __name__ = __name__

    def configure(self, **kwargs):
        ''' Convenience function to set a number of parameters on this logger
            and associated handlers and formatters.
        '''
        for kwarg in kwargs:
            value = kwargs[kwarg]

            if kwarg == 'level':
                self.set_level(value)

            elif kwarg == 'default_level':
                self.default_level = level_map.get(value, value)

            elif kwarg == 'datefmt':
                self.handlers[0].formatter.datefmt = value

            elif kwarg == 'msgfmt':
                self.handlers[0].formatter._style._fmt = value

            elif kwarg == 'stream':
                self.handlers[0].stream = value
                _, _, _, tlevel, is_a_tty = _find_palettes(value)
                # probably shouldn't auto configure theme, but it does,
                # skipping currently
                _add_handler(value, is_a_tty, tlevel, theme=None)

            elif kwarg == 'theme':
                if type(value) is str:
                    # this section should be reconciled with _add_handler
                    theme = _render_themes(self.handlers[0].stream)[value]
                    if value == 'plain':
                        fmtr = logging.Formatter(style='{', **theme)
                    elif value == 'json':
                        tlvl = self.handlers[0]._term_level
                        if is_fbterm:   hl = False          # doesn't work well
                        else:           hl = bool(tlvl)     # highlighting
                        fmtr = _JSONFormatter(term_level=tlvl, hl=hl, **theme)
                    else:
                        fmtr =  _ColorFormatter(**theme)
                elif type(value) is dict:
                    if 'style' in value or 'icons' in value:
                        fmtr =  _ColorFormatter(**theme)
                    else:
                        fmtr =  logging.Formatter(style='{', **theme)
                self.handlers[0].setFormatter(fmtr)

            elif kwarg == 'highlight':
                value = bool(value)
                if value is False:  # True value is a highlighter
                    self.handlers[0].formatter._highlight = value

            elif kwarg == 'icons':
                if type(value) is str:
                    value = _icons[value]
                self.handlers[0].formatter._theme_icons = value

            elif kwarg == 'style':
                if type(value) is str:
                    value = _render_styles(self.handlers[0].stream)[value]
                self.handlers[0].formatter._theme_style = value

            elif kwarg == 'lexer':
                try:
                    self.handlers[0].formatter.set_lexer(value)
                except AttributeError:
                    self.error('lexer: ColorFormatter not available.')
            else:
                raise NameError('unknown keyword argument: %s' % kwarg)

    def log_config(self):
        ''' Log the current logging configuration. '''
        level = self.level
        debug = self.debug
        debug('out logging config, version: %r', __version__)
        debug('  .name: {}, id: {}', self.name, hex(id(self)))
        debug('  .level: %s (%s)', level_map_int[level], level)
        debug('  .propagate: %s', self.propagate)
        debug('  .default_level: %s (%s)',
                   level_map_int[self.default_level], self.default_level)

        for i, handler in enumerate(self.handlers):
            fmtr = handler.formatter
            debug('  + Handler: %s %r', i, handler)
            debug('    + Formatter: %r', fmtr)
            debug('      .datefmt: %r', fmtr.datefmt)
            debug('      .msgfmt: %r', fmtr._fmt)
            debug('      fmt_style: %s', fmtr._style)
            debug('      theme.styles: %r', fmtr._theme_style)
            debug('      theme.icons: %r', fmtr._theme_icons)
            try:
                debug('      highlighting: %r, %r',
                    fmtr._lexer.__class__.__name__,
                    fmtr._hl_fmtr.__class__.__name__)
            except AttributeError:
                pass

    def setLevel(self, level):
        if type(level) is int:
            super().setLevel(level)
        else:
            super().setLevel(level_map.get(level.lower(), level))
    set_level = setLevel

    def __call__(self, message, *args):
        ''' Call logger directly, without function. '''
        if self.isEnabledFor(self.default_level):
            self._log(self.default_level, message, args)


def add_logging_level(name, value, method_name=None):
    ''' Comprehensively adds a new logging level to the ``logging`` module and
        the currently configured logging class.

        Derived from: https://stackoverflow.com/a/35804945/450917
    '''
    if not method_name:
        method_name = name.lower()

    # set levels
    logging.addLevelName(value, name)
    setattr(logging, name, value)
    level_map[name.lower()] = value

    if value == getattr(logging, 'EXCEPT', None):  # needs traceback added
        def logForLevel(self, message='', *args, **kwargs):
            show = kwargs.pop('show', True)
            if self.isEnabledFor(value):
                if show:
                    message = message.lstrip() + ' ▾\n'
                    message += traceback.format_exc()
                else:
                    message = message.lstrip()
                self._log(value, message, args, **kwargs)
    else:
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(value):
                self._log(value, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):  # may not need
        logging.log(value, message, *args, **kwargs)

    # set functions
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


def _add_handler(out_file, is_a_tty, level, theme='auto'):
    ''' Repeatable handler config. '''
    if is_fbterm:
        hl = False          # doesn't work well
    else:
        hl = level > 1    # highlighting > ANSI_MONOCHROME
    _handler = logging.StreamHandler(stream=out_file)

    if theme == 'auto':
        _theme_name = 'interactive' if is_a_tty else 'production'
        if os.environ.get('TERM') in ('linux', 'fbterm'):
            _theme_name = 'linux_' + _theme_name
        if os.name == 'nt':
            _theme_name = 'windows_' + _theme_name
        theme = _render_themes(out_file, fg=fg, bg=bg, fx=fx)[_theme_name]
    elif theme is None:
        try:
            fmtr = out.handlers[0].formatter
            theme = dict(
                icons=fmtr._theme_icons, style=fmtr._theme_style,
                fmt=fmtr._style._fmt, datefmt=fmtr.datefmt,
            )
        except AttributeError:
            theme = {}

    out.handlers = []  # clear any old
    _handler._term_level = level
    _formatter = _ColorFormatter(hl=hl, term_level=level, **theme)
    _handler.setFormatter(_formatter)
    out.addHandler(_handler)


# re-configure root logger
out = logging.getLogger()   # root
out.name = 'main'
out.__class__ = Logger      # one way to add call()

# odd level numbers chosen to avoid commonly configured variations
add_logging_level('TRACE', 7)
add_logging_level('NOTE', 27)
add_logging_level('EXCEPT', logging.ERROR + 3, 'exception')
add_logging_level('EXCEPT', logging.ERROR + 3, 'exc')
add_logging_level('FATAL', logging.FATAL)
level_map_int = {
    val: key
    for key, val in level_map.items()
}
out.warn = out.warning  # fix warn
out.set_level('note')

_add_handler(_out_file, _is_a_tty, _level)


# save original module for later, in case it's needed.
out._module = sys.modules[__name__]

# Wrap module with instance for direct access
sys.modules[__name__] = out
