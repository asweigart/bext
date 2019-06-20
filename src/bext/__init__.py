# Bext
# By Al Sweigart al@inventwithpython.com

__version__ = '0.0.4'

import random, sys
import curses # TODO - add some message if on windows and windows-curses isn't installed.

# NOTE: The screen goes away if an exception is raised, getting rid of potentially
# useful information. Maybe we should "save" the screen and display it before
# re-raising the exception.

ALL_FG_COLORS = ('black', 'blue', 'green', 'cyan', 'red', 'magenta', 'yellow', 'white',
                 'light black', 'light blue', 'light green', 'light cyan', 'light red',
                 'light magenta', 'light yellow', 'light white')
ALL_BG_COLORS = ('black', 'blue', 'green', 'cyan', 'red', 'magenta', 'yellow', 'white')

_ALL_CURSES_COLORS = [curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_GREEN,
                      curses.COLOR_CYAN, curses.COLOR_RED, curses.COLOR_MAGENTA,
                      curses.COLOR_YELLOW, curses.COLOR_WHITE]

# Initialize the curses library
_G_SCR = curses.initscr() # Initialize the screen.
curses.start_color() # Initialize colors.

# Initialize all the color pairs:
ALL_COLOR_PAIRS = {}
for fgi, fgc in enumerate(_ALL_CURSES_COLORS):
    for bgi, bgc in enumerate(_ALL_CURSES_COLORS):
        colorPairNum = 1 + (fgi + (bgi * 8))
        ALL_COLOR_PAIRS[(ALL_FG_COLORS[fgi], ALL_BG_COLORS[bgi])] = colorPairNum
        curses.init_pair(colorPairNum, _ALL_CURSES_COLORS[fgc], _ALL_CURSES_COLORS[bgc])

_G_CURRENT_FG_COLOR = 'white'
_G_CURRENT_BG_COLOR = 'black'

_G_SCR.scrollok(True) # When stuff is printed on the last line, scroll the window.
curses.noecho() # Don't echo key presses unless input() has been called. TODO - maybe not even then.
_G_SCR.keypad(True) #

def fg(color):
    """Sets the foreground color. The `color` parameter can be one of the
    following strings: 'random', 'black', 'blue', 'green', 'cyan', 'red',
    'magenta', 'yellow', 'white', 'light black', 'light blue', 'light green',
    'light cyan', 'light red', 'light magenta', 'light yellow', 'light white'."""
    global _G_CURRENT_FG_COLOR

    color = color.lower()
    if color == 'random':
        color = random.choice(ALL_FG_COLORS)

    if color not in ALL_FG_COLORS:
        raise ValueError('"%s" is not a valid color. Select one of %s' % (color, ', '.join(ALL_FG_COLORS)))

    _G_CURRENT_FG_COLOR = color


def bg(color):
    """Sets the background color. The `color` parameter can be one of the
    following strings: 'random', 'black', 'blue', 'green', 'cyan', 'red',
    'magenta', 'yellow', 'white'."""
    global _G_CURRENT_BG_COLOR
    color = color.lower()
    if color == 'random':
        color = random.choice(ALL_BG_COLORS)

    if color not in ALL_BG_COLORS:
        raise ValueError('"%s" is not a valid color. Select one of %s' % (color, ', '.join(ALL_BG_COLORS)))

    _G_CURRENT_BG_COLOR = color


def fgbg(fgcolor, bgcolor):
    """Sets the foreground and background color. This is a wrapper for calls
    to fg() and bg()."""
    try:
        fg(fgcolor)
    except:
        pass
    else:
        # Only call bg() if fg() was successful.
        bg(bgcolor)


def goto(x, y):
    """Repositions the cursor to the x, y coordinates in the terminal window.

    (0, 0) is the top-left corner coordinate."""
    x = 0 if x < 0 else x
    y = 0 if y < 0 else y
    _G_SCR.move(y, x)


def pos():
    """Get the current x, y position of the cursor."""
    y, x = curses.getsyx()
    return x, y


def charAt(x, y):
    """Return the character located at x, y on the screen."""
    bits = _G_SCR.inch(y, x)
    return


def fgAt(x, y):
    """Returns the foreground color at x, y on the screen."""
    bits = _G_SCR.inch(y, x)
    return


def bgAt(x, y):
    """Returns the background color at x, y on the screen."""
    bits = _G_SCR.inch(y, x)
    return


def resize(columns, rows):
    curses.resize_term(rows, columns)


def size():
    """Returns the size of the terminal as a named tuple of two ints: (width, height)"""
    height, width = _G_SCR.getmaxyx()
    return width, height


def clear(flush=True):
    """Clears the terminal and positions the cursor at the top-left corner."""
    _G_SCR.clear()

    if flush:
        _G_SCR.refresh()


def title(text):
    """Sets the title of the terminal window to text."""
    #sys.stdout.write(colorama.ansi.OSC + '2;' + text + colorama.ansi.BEL)
    #More info on how to do this on windows:
    #https://support.microsoft.com/en-us/help/124103/how-to-obtain-a-console-window-handle-hwnd
    pass


def hideCursor():
    """Hide the cursor."""
    curses.curs_set(False)


def showCursor():
    """Show the cursor."""
    curses.curs_set(True)


def blockCursor():
    """Show the full block style cursor."""
    curses.curs_set(2) # full block cursor


def print(*args, sep=' ', end='\n', flush=True):
    """TODO"""
    if sep is None:
        sep = ' '
    if not isinstance(sep, str):
        raise TypeError('sep must be None or a string, not %s' % sep.__class__.__name__)

    if end is None:
        end = '\n'
    if not isinstance(end, str):
        raise TypeError('end must be None or a string, not %s' % end.__class__.__name__)

    valueToPrint = sep.join([str(arg) for arg in args]) + end

    if _G_CURRENT_FG_COLOR.startswith('light'):
        nonLightColor = _G_CURRENT_FG_COLOR[6:]
        colorPairNum = ALL_COLOR_PAIRS[(nonLightColor, _G_CURRENT_BG_COLOR)]
        colorAndAttr = curses.color_pair(colorPairNum) | curses.A_BOLD
    else:
        colorPairNum = ALL_COLOR_PAIRS[(_G_CURRENT_FG_COLOR, _G_CURRENT_BG_COLOR)]
        colorAndAttr = curses.color_pair(colorPairNum)

    _G_SCR.addstr(valueToPrint, colorAndAttr)

    if flush:
        _G_SCR.refresh()


def input():
    """TODO"""
    pass
    curses.flushinp() # Get rid of any "type ahead" characters in the input buffer.


def exit(status=None):
    """TODO"""
    curses.endwin()
    sys.exit(status)

# Constants for hard-to-type (from an American, QWERTY-keyboard perspective) characters that exist in the Consolas (Windows), Menlo (macOS), and Monospace Regular (Ubuntu) fonts.
# TODO - fill in the rest based on the Consolas, Menlo, and Monospace Regular fonts.
"""
CENT = chr(162) # ¢
POUND = chr(163) # £
YEN = chr(165) # ¥
BROKEN_BAR = chr(166) # ¦
SECTION = chr(167) # §
COPYRIGHT = chr(169) # ©
"""

