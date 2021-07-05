'''
    out - Simple logging with a few fun features.
    © 2018-19, Mike Miller - Released under the LGPL, version 3+.

    This module contains themes for colors, icons, message and date formats.
    They can be used separately, or together as a "full" theme.

    Unicode symbols are used throughout as "icons" for increased readability and
    conciseness.

    They are/should be padded to two characters due to some glyphs being wide.
    Width can be looked up, e.g.::

        >>> unicodedata.east_asian_width('💀')
        'W'
'''
from .detection import _find_palettes, is_fbterm

icons = dict(

    symbol = dict(
        TRACE    = '• ',
        DEBUG    = '• ',
        INFO     = '✓ ',
        NOTE     = '🎗 ',
        WARNING  = '⚠ ',
        ERROR    = '✗ ',
        EXCEPT   = '💣',
        CRITICAL = '💀',
        FATAL    = '💀',
        NOTSET   = '␀ ',
    ),
    circled_lower = dict(
        TRACE    = 'ⓣ',
        DEBUG    = 'ⓓ',
        INFO     = 'ⓘ',
        NOTE     = 'ⓝ',
        WARNING  = 'ⓦ',
        ERROR    = 'ⓔ',
        EXCEPT   = 'ⓧ',
        CRITICAL = 'ⓕ',
        FATAL    = 'ⓕ',
        NOTSET   = 'ⓝ',
    ),
    ascii = dict(
        TRACE    = 'T',
        DEBUG    = 'D',
        INFO     = 'I',
        NOTE     = 'N',
        WARNING  = 'W',
        ERROR    = 'E',
        EXCEPT   = 'X',
        CRITICAL = 'F',
        FATAL    = 'F',
        NOTSET   = 'N',
    ),
    ascii_symbol = dict(
        TRACE    = '-',
        DEBUG    = '~',
        INFO     = '=',
        NOTE     = '+',
        WARNING  = '!',
        ERROR    = '*',
        EXCEPT   = '*',
        CRITICAL = '!',
        FATAL    = '!',
        NOTSET   = '_',
    ),
    circled = dict(
        TRACE    = '🅣',
        DEBUG    = '🅓',
        INFO     = '🅘',
        NOTE     = '🅝',
        WARNING  = '🅦',
        ERROR    = '🅔',
        EXCEPT   = '🅧',
        CRITICAL = '🅕',
        FATAL    = '🅕',
        NOTSET   = '🅝',
    ),
    rounded = dict(
        TRACE    = '🆃',
        DEBUG    = '🅳',
        INFO     = '🅸',
        NOTE     = '🅽',
        WARNING  = '🆆',
        ERROR    = '🅴',
        EXCEPT   = '🆇',
        CRITICAL = '🅵',
        FATAL    = '🅵',
        NOTSET   = '🅽',
    ),
)


def render_styles(out_file, fg=None, bg=None, fx=None):
    ''' Styles need to react to changes in output stream. Therefore they are
        rendered here with (or without) escape sequences as needed.

        Most of the time, this will only be done once.
    '''
    if not (fg and bg and fx):  # find once
        fg, bg, fx, _CHOSEN_PALETTE, _is_a_tty  = _find_palettes(out_file)

    # render styles first
    _fatal_clr = fg.lightwhite
    _fatal_clr_bld = fx.bold + fg.white

    styles = dict(
        norm = dict(
            TRACE    = str(fg.purple),
            DEBUG    = str(fg.blue),
            INFO     = str(fg.green),
            NOTE     = str(fg.lightcyan),
            WARNING  = str(fg.lightyellow),
            ERROR    = str(fg.red),
            EXCEPT   = str(fg.lightred),
            CRITICAL = str(_fatal_clr),
            FATAL    = str(_fatal_clr),
            NOTSET   = '',
        ),
        reverse = dict(
            TRACE    = str(fg.purple + fx.reverse),
            DEBUG    = str(fg.blue + fx.reverse),
            INFO     = str(fg.green + fx.reverse),
            NOTE     = str(fg.lightcyan + fx.reverse),
            WARNING  = str(fg.lightyellow + fx.reverse),
            ERROR    = str(fg.red + fx.reverse),
            EXCEPT   = str(fg.lightred + fx.reverse),
            CRITICAL = str(_fatal_clr + fx.reverse),
            FATAL    = str(_fatal_clr + fx.reverse),
            NOTSET   = '',
        ),
        bold = dict(
            TRACE    = str(fg.purple),
            DEBUG    = str(fg.blue),
            INFO     = str(fg.green),
            NOTE     = str(fg.cyan + fx.bold),
            WARNING  = str(fg.yellow + fx.bold),
            ERROR    = str(fg.red + fx.bold),
            EXCEPT   = str(fg.red + fx.bold),
            CRITICAL = str(_fatal_clr_bld),
            FATAL    = str(_fatal_clr_bld),
            NOTSET   = '',
        ),
        reverse_fbterm = dict(  # bright limits, use bg with first of 256
            TRACE    = str(fg.purple + fx.reverse),
            DEBUG    = str(fg.blue + fx.reverse),
            INFO     = str(fg.green + fx.reverse),
            NOTE     = fg.black + bg.i14,  # already strings, don't mix
            WARNING  = fg.black + bg.i11,
            ERROR    = fg.black + bg.i9,
            EXCEPT   = fg.black + bg.i9,
            CRITICAL = fg.black + bg.i15,
            FATAL    = fg.black + bg.i15,
            NOTSET   = '',
        ),
        mono = dict(
            TRACE    = str(fx.dim),
            DEBUG    = str(fx.dim),
            INFO     = '',
            NOTE     = str(fx.italic),
            WARNING  = str(fx.italic),
            ERROR    = str(fx.bold),
            EXCEPT   = str(fx.bold),
            CRITICAL = str(fx.bold + fx.reverse),
            FATAL    = str(fx.bold + fx.reverse),
            NOTSET   = '',
        ),
    )
    _blink = styles['norm'].copy()
    _blink['FATAL'] = str(_fatal_clr + fx.blink)
    styles['blink'] = _blink

    return styles


def render_themes(out_file, fg=None, bg=None, fx=None):
    ''' Themes need to react to changes in output stream. Therefore they are
        rendered here with or without escape sequences as needed.
    '''
    if not (fg and bg and fx):
        fg, bg, fx, _CHOSEN_PALETTE, _is_a_tty  = _find_palettes(out_file)

    styles = render_styles(out_file, fg=fg, bg=bg, fx=fx)

    # uggh - fbterm escape sequences conflict with brace formatting :-/
    dark_grey = str(fg.i242)
    drk_grey4 = str(fg.lightblack)  # 16 color
    medm_grey = str(fg.i245)
    int_green = str(fg.green)
    end = str(fx.end)
    if is_fbterm:
        dark_grey += '}'
        drk_grey4 = dark_grey  # too dark
        medm_grey += '}'

    # these are full themes, colors, icons, msg and date formats
    themes = dict(
        interactive = dict(
            style = styles['norm'],
            icons = icons['rounded'],
            fmt='  {on}{icon:<2}{off} ' +
                dark_grey + '{name}/' +
                medm_grey + '{funcName}:' +
                int_green + '{lineno:<3}' + end +
                ' {message}',
            datefmt='%H:%M:%S',
        ),

        production = dict(
            style = None,
            icons = icons['ascii_symbol'],
            fmt='{asctime}.{msecs:03.0f} {icon} {levelname:<7} '
                '{name}/{funcName}:{lineno} {message}',
            datefmt='%Y-%m-%d %H:%M:%S',
        ),

        plain = dict(
            fmt='{asctime}.{msecs:03.0f} {levelname:<7} {name}/{funcName}:{lineno}'
                ' {message}',
            datefmt='%Y-%m-%d %H:%M:%S',
        ),

        json = dict(
            fmt='asctime,msecs,levelname,name,funcName,lineno,message',
            datefmt='%Y-%m-%d %H:%M:%S',
        ),

        mono = dict(
            datefmt='%Y-%m-%d %H:%M:%S',
            style='mono',
            fmt='{asctime}.{msecs:03.0f} {on}{levelname:<7} '
                '{name}/{funcName}:{lineno} {message}{off}',
        ),

        linux_interactive = dict(
            style = styles['reverse'],
            icons = icons['ascii'],
            fmt='  {on}{icon}{off} ' +
                drk_grey4 + '{name}/{funcName}:' +
                int_green + '{lineno:<3}' + end +
                ' {message}',
        ),
        linux_production = dict(
            style = styles['norm'],
            icons = None,
            fmt='{asctime}.{msecs:03.0f} {on}{levelname:<7}{off} '
                '{name}/{funcName}:{lineno} {message}',
        ),

    )
    themes['windows_interactive'] = themes['linux_interactive']
    #~ if os_name == 'nt':     # unicode for Win Terminal support
        #~ import locale       # exposes display bug - deactivated for now
        #~ if locale.getpreferredencoding() == 'cp65001':  # utf8
            #~ themes['windows_interactive']['style'] = styles['norm']
            #~ themes['windows_interactive']['icons'] = icons['rounded']

    themes['windows_production'] = themes['production']
    if is_fbterm:
        themes['linux_interactive']['style'] = styles['reverse_fbterm']

    return themes
