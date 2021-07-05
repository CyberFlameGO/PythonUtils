'''
    out - Simple logging with a few fun features.
    © 2018-19, Mike Miller - Released under the LGPL, version 3+.

    Message template variables:

        {name}              Name of the logger (logging channel)
        {levelno}           Numeric logging level for the message (DEBUG, INFO,
                                WARNING, ERROR, CRITICAL)
        {levelname}         Text logging level for the message ("DEBUG", "INFO",
                                "WARNING", "ERROR", "CRITICAL")
        {pathname}          Full pathname of the source file where the logging
                                call was issued (if available)
        {filename}          Filename portion of pathname
        {module}            Module (name portion of filename)
        {lineno)d           Source line number where the logging call was issued
                                (if available)
        {funcName}          Function name
        {created}           Time when the LogRecord was created (time.time()
                                return value)
        {asctime}           Textual time when the LogRecord was created
        {msecs}             Millisecond portion of the creation time
        {relativeCreated}   Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        {thread}            Thread ID (if available)
        {threadName}        Thread name (if available)
        {process}           Process ID (if available)
        {message}           The result of record.getMessage(), computed just as
                                the record is emitted

        # added:
        {on}…{off}          Toggles level-specific style (colors, etc) support.
        {icon}              Level-specific icon.
'''
import logging
import re
from pprint import pformat

from . import themes
from . import fx
from . import highlight
from .detection import is_fbterm

DATA_SEARCH_LIMIT = 80
_end = str(fx.end)
if is_fbterm:  # fbterm esc seqs conflict with brace formatting :-/
    _end = _end.replace('}', '}}')

json_data_search = re.compile(r"(\{|\[|')").search
xml_data_search = re.compile(r"(<|')").search
pyt_data_search = re.compile(r"(\{|\[|\(|:|;)").search


class ColorFormatter(logging.Formatter):
    ''' Colors the level-name of a log message according to the level.

        Arguments:

            datefmt         - strftime datetime template
            fmt             - log template
            icons           - dict of level:value for icons
            style           - dict of level:value for terminal style
            template_style  - log template syntax: %, {, $

            # highlighting
            hl              - bool, highlight the message.
            lexer           - None, or Pygment's lexer: python3', 'json', etc.
            hl_formatter    - None, or pass a configured Pygments formatter.
            code_indent     - If highlighting data with newlines, indent N sp.
    '''
    default_msec_format = '%s.%03d'  # use period decimal point

    def __init__(self,
            code_indent=12,
            datefmt=None,
            fmt=None,
            hl=True,
            hl_formatter=None,
            term_level=None,
            icons=None,
            lexer='python3',
            style=None,
            template_style='{',
        ):
        self._theme_style = (
            style if style else themes.render_styles(term_level)['norm']
        )
        self._theme_icons = icons if icons else themes.icons['rounded']
        self._code_indent = code_indent
        self._highlight = self._lexer = None
        if hl:
            if lexer:
                self._highlight = highlight.highlight
                self.set_lexer(lexer)
            self._hl_fmtr = hl_formatter or highlight.get_term_formatter(term_level)

        super().__init__(fmt=fmt, datefmt=datefmt, style=template_style)

    def set_lexer(self, name):
        if highlight.get_lexer_by_name:
            self._lexer = highlight.get_lexer_by_name(name)
            self._lexer.ensurenl = False
        if name == 'xml':
            self.data_search = xml_data_search
        elif name == 'json':
            self.data_search = json_data_search
        else:
            self.data_search = pyt_data_search

    def format(self, record):
        ''' Log color formatting. '''
        levelname = record.levelname    # len7 limit
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        if record.funcName == '<module>':
            record.funcName = ''

        # render the message part with arguments
        try:  # Allow {} style - need a faster way to determine this:
            message = record.getMessage()
        except TypeError:
            message = record.msg.format(*record.args)

        # decide to highlight w/ pygments
        # TODO: Highlight args directly and drop text scan? - didn't work well.
        if self._highlight:
            match = self.data_search(message, 0, DATA_SEARCH_LIMIT)
            if match:
                pos = match.start()
                front, back = message[:pos], message[pos:]  # Spliten-Sie
                if front.endswith('\n'):                    # indent data?
                    back = pformat(record.args)
                    back = left_indent(back, self._code_indent)
                back = self._highlight(back, self._lexer, self._hl_fmtr)
                message = f'{front}{back}'

        # style the level, icon
        record.message = message
        record.on = self._theme_style.get(levelname, '')
        record.icon = self._theme_icons.get(levelname, '')
        record.off = _end
        s = self.formatMessage(record)

        # this needs to be here, Formatter class not very granular.
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


class JSONFormatter(logging.Formatter):
    '''
        Formats a log message into line-oriented JSON.

        The message template format is different.
        It uses simple CSV (no spaces allowed) to define field order, e.g.:

            fmt='asctime,msecs,levelname,name,funcName,lineno,message'

        (Currently field order requires Python 3.6, but could be backported.)
    '''
    def __init__(self, datefmt=None, fmt=None, term_level=None, hl=True,
                 hl_formatter=None):
        self._fields = fmt.split(',')
        from json import dumps
        self.dumps = dumps
        self._highlight = None
        if hl:
            self._highlight = highlight.highlight
            if self._highlight:
                self._lexer = highlight.get_lexer_by_name('JSON')
                self._hl_formatter = (
                    hl_formatter or highlight.get_term_formatter(term_level)
                )
        try:
            super().__init__(fmt=fmt, datefmt=datefmt)
        except ValueError:  # py 3.8 :-/
            super().__init__(fmt=fmt, datefmt=datefmt, validate=False)

    def format(self, record):
        ''' Log color formatting. '''
        levelname = record.levelname
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        record.asctime = self.formatTime(record, self.datefmt)

        # render the message part with arguments
        try:  # Allow {} style - need a faster way to determine this:
            message = record.getMessage()
        except TypeError:
            message = record.msg.format(*record.args)
        record.message = message

        fields = self._fields
        data = { name: getattr(record, name) for name in fields }
        if 'asctime' in fields and 'msecs' in fields:  # needs option for this
            data['asctime'] += '.{:03.0f}'.format(data.pop('msecs'))
        s = self.dumps(data)
        if self._highlight:
            s = self._highlight(s, self._lexer, self._hl_formatter).rstrip()

        # this needs to be here, Formatter class isn't very extensible.
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


def left_indent(text, indent=12, end='\n'):
    ''' A bit of the ol' ultraviolence  :-/ '''
    indent = ' ' * indent
    lines = [indent + line for line in text.splitlines(True)]
    lines.append(end)
    return ''.join(lines)
