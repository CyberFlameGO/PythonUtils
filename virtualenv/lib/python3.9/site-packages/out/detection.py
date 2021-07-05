'''
    out - Simple logging with a few fun features.
    © 2018-19, Mike Miller - Released under the LGPL, version 3+.
'''
from console.constants import TermLevel
from console.detection import init, is_a_tty, is_fbterm, os_name
from console.style import ForegroundPalette, BackgroundPalette, EffectsPalette


def _find_palettes(stream):
    ''' Need to configure palettes manually, since we are checking stderr. '''
    level = init(_stream=stream)
    fg = ForegroundPalette(level=level)
    bg = BackgroundPalette(level=level)
    fx = EffectsPalette(level=level)

    return fg, bg, fx, level, is_a_tty(stream)


TermLevel, is_fbterm, os_name  # quiet pyflakes
