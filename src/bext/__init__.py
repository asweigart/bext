# -*- coding: utf-8 -*-
# Bext
# By Al Sweigart al@inventwithpython.com
# Copyright 2019, BSD 3-Clause license, see LICENSE file.
# Built on top of Colorama by Jonathan Hartley


__version__ = '0.0.6'

import colorama, sys, os, random, shutil

ALL_COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')


if sys.platform == 'win32':
    import msvcrt  # Used by getKey()
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        pass

    COORD._fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
else:
    # macOS and Linux
    import tty, termios  # Used by getKey()



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
    # On macOS and Linux, clearing doesn't reset the cursor back to the top-left
    # corner of the termnal window, so do that here:
    goto(0, 0)

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


def _getKey_win32_api():
    """Block until a single key is pressed, then return the key as a string.

    This function can't detect ctrl, shift, alt, win, or other special keys.
    However, holding down shift or having capslock engaged will return a
    shifted character."""
    if sys.version_info[0] == 2:
        getchFunc = msvcrt.getch
    else:
        getchFunc = msvcrt.getwch

    key = getchFunc()

    if key == '\r':
        # Automatically convert \r to \n. It just makes sense to me.
        # Nobody uses \r and they'll probably expect \n.
        return '\n'
    elif key == '\x1b':
        return 'esc'  # Esc key.
    elif key == chr(224):
        key2 = getchFunc()
        return {
            chr(224) + 'I': 'pgup',
            chr(224) + 'Q': 'pgdn',
            chr(224) + 'O': 'end',
            chr(224) + 'G': 'home',
            chr(224) + 'R': 'insert',
            chr(224) + 'S': 'del',
            chr(224) + 'K': 'left',
            chr(224) + 'H': 'up',
            chr(224) + 'P': 'down',
            chr(224) + 'M': 'right',
            chr(224) + '\x85': 'f11',
            chr(224) + '\x86': 'f12',
            }.get(key + key2, key + key2)
    elif key == '\x00':
        key2 = getchFunc()
        return {
            '\x00' + ';': 'f1',
            '\x00' + '<': 'f2',
            '\x00' + '=': 'f3',
            '\x00' + '>': 'f4',
            '\x00' + '?': 'f5',
            '\x00' + '@': 'f6',
            '\x00' + 'A': 'f7',
            '\x00' + 'B': 'f8',
            '\x00' + 'C': 'f9',
            '\x00' + 'D': 'f10',
            }.get(key + key2, key + key2)
    else:
        return key  # Return the key as is.


def _getKey_posix_api():
    # TODO - test this
    # From https://code.activestate.com/recipes/577977-get-single-keypress/
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



# https://en.wikipedia.org/wiki/Windows_Glyph_List_4
allChrs = {}
allOrds = {}
for start, stop in ((0x21, 0x7f), (0xa1, 0x180), (0x192, 0x193), (0x1fa, 0x200), (0x2c6, 0x2c8), (0x2c9, 0x2ca),
    (0x2d8, 0x2de), (0x384, 0x38b), (0x38c, 0x38d), (0x38e, 0x3a2), (0x3a3, 0x3cf), (0x400, 0x492), (0x1e80, 0x1e86),
    (0x1ef2, 0x1ef4), (0x2013, 0x2016), (0x2017, 0x201f), (0x2020, 0x2023), (0x2026, 0x2027), (0x2030, 0x2031),
    (0x2032, 0x2034), (0x2039, 0x203b), (0x203c, 0x203d), (0x203e, 0x203f), (0x2044, 0x2045), (0x207f, 0x2080),
    (0x20a3, 0x20a5), (0x20a7, 0x20a8), (0x20ac, 0x20ad), (0x2105, 0x2106), (0x2113, 0x2114), (0x2116, 0x2117),
    (0x2122, 0x2123), (0x2126, 0x2127), (0x212e, 0x212f), (0x215b, 0x215f), (0x2190, 0x2196), (0x21a8, 0x21a9),
    (0x2202, 0x2203), (0x2206, 0x2207), (0x220f, 0x2210), (0x2211, 0x2213), (0x2215, 0x2216), (0x2219, 0x221b),
    (0x221e, 0x2220), (0x2229, 0x222a), (0x222b, 0x222c), (0x2248, 0x2249), (0x2260, 0x2262), (0x2264, 0x2266),
    (0x2302, 0x2303), (0x2310, 0x2311), (0x2320, 0x2322), (0x2500, 0x2501), (0x2502, 0x2503), (0x250c, 0x250d),
    (0x2510, 0x2511), (0x2514, 0x2515), (0x2518, 0x2519), (0x251d, 0x251e), (0x2524, 0x2525), (0x252c, 0x252d),
    (0x2534, 0x2535), (0x253c, 0x253d), (0x2550, 0x256d), (0x2580, 0x2581), (0x2584, 0x2585), (0x2588, 0x2589),
    (0x258c, 0x258d), (0x2590, 0x2594), (0x25a0, 0x25a2), (0x25aa, 0x25ad), (0x25b4, 0x25b5), (0x25ba, 0x25bb),
    (0x25bc, 0x25bd), (0x25c4, 0x25c5), (0x25ca, 0x25cc), (0x25cf, 0x25d0), (0x25d8, 0x25da), (0x25e6, 0x25e7),
    (0x263a, 0x263d), (0x2640, 0x2641), (0x2642, 0x2643), (0x2660, 0x2661), (0x2663, 0x2664), (0x2665, 0x2667),
    (0x266a, 0x266c)):
        for i in range(start, stop):
            allChrs[i] = chr(i)
            allOrds[chr(i)] = i


if sys.platform == 'win32':
    # On Windows, use the win32 api to set the cursor position since it's faster.
    goto = _goto_win32_api
    getKey = _getKey_win32_api
else:
    goto = _goto_control_code

init() # Automatically called on import.
