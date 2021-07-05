'''
    out - Simple logging with a few fun features.
    © 2018-19, Mike Miller - Released under the LGPL, version 3+.

    Highlighting with Pygments!
'''
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.token import (Keyword, Name, Comment, String, Error,
                                Number, Operator, Punctuation,
                                Token, Generic, Whitespace)
except ImportError:
    highlight = get_lexer_by_name = None

from .detection import TermLevel


def get_term_formatter(level):
    ''' Build formatter according to environment. '''

    term_formatter = None
    if level and highlight:

        if level >= TermLevel.ANSI_EXTENDED:

            from pygments.formatters import Terminal256Formatter
            from pygments.style import Style

            class OutStyle(Style):
                styles = {
                    Comment:                'italic ansibrightblack',
                    Keyword:                'bold #4ac',  # light blue
                    Keyword.Constant:       'nobold #3aa',  # ansicyan
                    Number:                 'ansigreen',

                    Name.Tag:               '#4ac',  # light blue, xml, json
                    Name.Attribute:         '#4ac',  # light blue

                    Operator:               'nobold #b94',
                    Operator.Word:          'bold #4ac',
                    Punctuation:            'nobold #b94',

                    String:                 'ansibrightmagenta',  # amber
                    Generic.String:         'ansired',
                }
            term_formatter = Terminal256Formatter(style=OutStyle)

        elif level >= TermLevel.ANSI_BASIC:

            from pygments.formatters import TerminalFormatter

            _default = ('', '')
            color_scheme = {
                Comment.Preproc:    _default,
                Name:               _default,
                Token:              _default,
                Whitespace:         _default,
                Generic.Heading:    ('**',                  '**'),

                Comment:            ('brightblack',         'brightblack'),
                Keyword:            ('*brightblue*',        '*brightblue*'),
                Keyword.Constant:   ('cyan',                'cyan'),
                Keyword.Type:       ('cyan',                'cyan'),
                Operator:           ('yellow',              'yellow'),
                Operator.Word:      ('*brightblue*',        '*brightblue*'),

                Name.Builtin:       ('cyan',                'cyan'),
                Name.Decorator:     ('magenta',             'magenta'),
                Name.Tag:           ('brightblue',          'brightblue'),
                Name.Attribute:     ('brightblue',          'brightblue'),

                String:             ('brightmagenta',       'brightmagenta'),
                Number:             ('green',               'green'),

                Generic.Deleted:    ('red',                 'brightred'),
                Generic.Inserted:   ('green',               'brightgreen'),
                Generic.Error:      ('brightred',           'brightred'),

                Error:              ('_brightred_',         '_brightred_'),
            }

            term_formatter = TerminalFormatter(
                bg='dark',
                colorscheme=color_scheme,
            )

    return term_formatter
