# -*- coding: utf-8 -*-
# Bext
# By Al Sweigart al@inventwithpython.com
# Copyright 2019, BSD 3-Clause license, see LICENSE file.
# Built on top of Colorama by Jonathan Hartley


__version__ = '0.0.5'

import colorama, sys, os, random, shutil

ALL_COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')


if sys.platform == 'win32':
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        pass

    COORD._fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]




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


def _goto_control_code(x, y):
    """Repositions the cursor to the x, y coordinates in the terminal window.

    (0, 0) is the top-left corner coordinate."""
    if x < 0:
        raise IndexError('x coordinate is negative')
    if y < 0:
        raise IndexError('y coordinate is negative')

    width, height = shutil.get_terminal_size()

    if x >= width:
        raise IndexError('x coordinate is greater than terminal width ' + str(width))
    if y >= height:
        raise IndexError('y coordinate is greater than terminal height ' + str(height))

    sys.stdout.write('\x1b[%d;%dH' % (y + 1, x + 1))


def _goto_win32_api(x, y):
    """Repositions the cursor to the x, y coordinates in the terminal window.

    (0, 0) is the top-left corner coordinate."""
    if x < 0:
        raise IndexError('x coordinate is negative')
    if y < 0:
        raise IndexError('y coordinate is negative')

    width, height = shutil.get_terminal_size()

    if x >= width:
        raise IndexError('x coordinate is greater than terminal width ' + str(width))
    if y >= height:
        raise IndexError('y coordinate is greater than terminal height ' + str(height))

    h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleCursorPosition(h, COORD(x, y))


def resize(columns, rows):
    if sys.platform == 'win32':
        # This is only on Windows 7 and later.
        os.system('mode %s,%s' % (columns, rows))
        return size() == (columns, rows)
        # TODO - figure out a way to detect windows 7. (There seems to be some problems with platform.platform())
    else:
        raise NotImplementedError
        #os.system('resize -s %s %s' % (rows, columns))
        #return size() == (columns, rows)


def size():
    """Returns the size of the terminal as a named tuple of two ints: (columns, rows)"""
    return shutil.get_terminal_size()


def width():
    """Returns the width of the terminal as an int."""
    return shutil.get_terminal_size()[0]


def height():
    """Returns the height of the terminal as an int."""
    return shutil.get_terminal_size()[1]


def clear(mode=2):
    """Clears the terminal and positions the cursor at the top-left corner."""
    sys.stdout.write(colorama.ansi.CSI + str(mode) + 'J')


def title(text):
    """Sets the title of the terminal window to text."""
    sys.stdout.write(colorama.ansi.OSC + '2;' + text + colorama.ansi.BEL)


def hide():
    if sys.platform == 'win32':
        # This only works in the Command Prompt and PowerShell, not in other terminal-like environments.
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    else:
        # I can't get this to work for some reason.
        #sys.out.write('\033[?25l')
        #sys.out.flush()
        raise NotImplementedError

def show():
    if sys.platform == 'win32':
        # This only works in the Command Prompt and PowerShell, not in other terminal-like environments.
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        #sys.out.write('\033[?25h')
        #sys.out.flush()
        raise NotImplementedError

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

if sys.platform == 'win32':
    # On Windows, use the win32 api to set the cursor position since it's faster.
    goto = _goto_win32_api
else:
    goto = _goto_control_code

init() # Automatically called on import.
