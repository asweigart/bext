# Bext
# By Al Sweigart al@inventwithpython.com
# Copyright 2019, BSD 3-Clause license, see LICENSE file.
# Built on top of Colorama by Jonathan Hartley


__version__ = '0.0.2'

import colorama, sys, os, random

ALL_COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')

def init():
    """This sets up stdout to work in color. This function is automatically
    called when Bext is imported."""
    colorama.init()


def fg(color):
    """Sets the foreground color. The `color` parameter can be one of the
    following strings: 'black', 'red', 'green', 'yellow', 'blue', 'purple',
    'cyan', 'white', 'reset'."""
    color = color.lower()
    if color == 'random':
        color = random.choice(ALL_COLORS)

    color = {'black':   colorama.Fore.BLACK,
             'red':     colorama.Fore.RED,
             'green':   colorama.Fore.GREEN,
             'yellow':  colorama.Fore.YELLOW,
             'blue':    colorama.Fore.BLUE,
             'magenta': colorama.Fore.MAGENTA,
             'purple':  colorama.Fore.MAGENTA,
             'cyan':    colorama.Fore.CYAN,
             'white':   colorama.Fore.WHITE,
             'reset':   colorama.Fore.RESET}[color]
    sys.stdout.write(color)


def bg(color):
    """Sets the background color. The `color` parameter can be one of the
    following strings: 'black', 'red', 'green', 'yellow', 'blue', 'purple',
    'cyan', 'white', 'reset'."""
    color = color.lower()
    if color == 'random':
        color = random.choice(ALL_COLORS)

    color = {'black':   colorama.Back.BLACK,
             'red':     colorama.Back.RED,
             'green':   colorama.Back.GREEN,
             'yellow':  colorama.Back.YELLOW,
             'blue':    colorama.Back.BLUE,
             'magenta': colorama.Back.MAGENTA,
             'purple':  colorama.Back.MAGENTA,
             'cyan':    colorama.Back.CYAN,
             'white':   colorama.Back.WHITE,
             'reset':   colorama.Back.RESET}[color]
    sys.stdout.write(color)


def goto(x, y):
    """Repositions the cursor to the x, y coordinates in the terminal window.

    (0, 0) is the top-left corner coordinate."""
    x = 0 if x < 0 else x
    y = 0 if y < 0 else y
    sys.stdout.write('\x1b[%d;%dH' % (y + 1, x + 1))


def size():
    """Returns the size of the terminal as a named tuple of two ints: (columns, lines)"""
    return os.get_terminal_size()


def clear(mode=2):
    """Clears the terminal and positions the cursor at the top-left corner."""
    sys.stdout.write(colorama.ansi.CSI + str(mode) + 'J')


def title(text):
    """Sets the title of the terminal window to text."""
    sys.stdout.write(colorama.ansi.OSC + '2;' + text + colorama.ansi.BEL)


init() # Automatically called on import.
