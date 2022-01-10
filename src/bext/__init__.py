# -*- coding: utf-8 -*-
# Bext
# By Al Sweigart al@inventwithpython.com
# Copyright 2019, BSD 3-Clause license, see LICENSE file.
# Built on top of Colorama by Jonathan Hartley


__version__ = '0.0.8'

import colorama, sys, os, random, shutil
from contextlib import contextmanager

ALL_COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')

class BextException(Exception):
    """Raised by the code in this getkey module. If getkey ever raises
    an exception that isn't BextException, you can assume it's caused
    by a bug in the getkey module."""
    pass


commonCodeToNameMapping = {
    '\x00': 'null',
    '\x01': 'start of heading',
    '\x02': 'start of text',
    '\x03': 'end of text',
    '\x04': 'end of transmission',
    '\x05': 'enquiry',
    '\x06': 'acknowledge',
    '\x07': 'bell',
    '\x08': '\b',
    '\t': '\t',
    '\n': '\n',
    '\x0b': 'vertical tab',
    '\x0c': 'new page',
    '\r': '\n',  # Uniformly calling \r and \n a newline.
    '\x0e': 'shift out',
    '\x0f': 'shift in',
    '\x10': 'data link escape',
    '\x11': 'device control 1',
    '\x12': 'device control 2',
    '\x13': 'device control 3',
    '\x14': 'device control 4',
    '\x15': 'negative acknowledge',
    '\x16': 'synchronous idle',
    '\x17': 'end of transmission block',
    '\x18': 'cancel',
    '\x19': 'end of medium',
    '\x1a': 'substitute',
    '\x1b': 'esc',
    '\x1c': 'file separator',
    '\x1d': 'group separator',
    '\x1e': 'record separator',
    '\x1f': 'unit separator',
    ' ': ' ',
    '!': '!',
    '"': '"',
    '#': '#',
    '$': '$',
    '%': '%',
    '&': '&',
    "'": "'",
    '(': '(',
    ')': ')',
    '*': '*',
    '+': '+',
    ',': ',',
    '-': '-',
    '.': '.',
    '/': '/',
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    ':': ':',
    ';': ';',
    '<': '<',
    '=': '=',
    '>': '>',
    '?': '?',
    '@': '@',
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 'P',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',
    '[': '[',
    '\\': '\\',
    ']': ']',
    '^': '^',
    '_': '_',
    '`': '`',
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',
    '{': '{',
    '|': '|',
    '}': '}',
    '~': '~',
    # The following have codes that are already used:
    #'\x01': 'ctrl-a',
    #'\x02': 'ctrl-b',
    #'\x03': 'ctrl-c',
    #'\x04': 'ctrl-d',
    #'\x05': 'ctrl-e',
    #'\x06': 'ctrl-f',
    #'\x07': 'ctrl-g',
    #'\x08': 'ctrl-h',
    #'\t': 'ctrl-i',
    #'\n': 'ctrl-j',
    #'\x0b': 'ctrl-k',
    #'\x0c': 'ctrl-l',
    #'\r': 'ctrl-m',
    #'\x0e': 'ctrl-n',
    #'\x0f': 'ctrl-o',
    #'\x10': 'ctrl-p',
    #'\x11': 'ctrl-q',
    #'\x12': 'ctrl-r',
    #'\x13': 'ctrl-s',
    #'\x14': 'ctrl-t',
    #'\x15': 'ctrl-u',
    #'\x16': 'ctrl-v',
    #'\x17': 'ctrl-w',
    #'\x18': 'ctrl-x',
    #'\x19': 'ctrl-y',
    #'\x1a': 'ctrl-z',
    #'\x00': 'ctrl-at',
    #'\x1c': 'ctrl-backslash',
    #'\x1e': 'ctrl-caret',
    #'\x1b': 'ctrl-left-bracket',
    #'\x1d': 'ctrl-right-bracket',
    #'\x1f': 'ctrl-underscore',
}


windowsCodeToNameMapping = {
    '\xe0K': 'left',
    '\xe0M': 'right',
    '\xe0H': 'up',
    '\xe0P': 'down',
    '\x00;': 'f1',
    '\x00<': 'f2',
    '\x00=': 'f3',
    '\x00>': 'f4',
    '\x00?': 'f5',
    '\x00@': 'f6',
    '\x00A': 'f7',
    '\x00B': 'f8',
    '\x00C': 'f9',
    '\x00D': 'f10',
    '\xe0\x85': 'f11',
    '\xe0\x86': 'f12',
    '\xe0R': 'insert',
    '\xe0S': 'delete',
    '\xe0I': 'pgup',
    '\xe0Q': 'pgdn',
    '\xe0G': 'home',
    '\xe0O': 'end',
    '\x00^': 'ctrl-f1',
    '\x00_': 'ctrl-f2',
    '\x00`': 'ctrl-f3',
    '\x00a': 'ctrl-f4',
    '\x00b': 'ctrl-f5',
    '\x00c': 'ctrl-f6',
    '\x00d': 'ctrl-f7',
    '\x00e': 'ctrl-f8',
    '\x00f': 'ctrl-f9',
    '\x00g': 'ctrl-f10',
    '\xe0\x89': 'ctrl-f11',
    '\xe0\x8a': 'ctrl-f12',
    '\x00\x03': 'ctrl-2',
    '\xe0\x8d': 'ctrl-up',
    '\xe0\x91': 'ctrl-down',
    '\xe0s': 'ctrl-left',
    '\xe0t': 'ctrl-right',
    '\x00\x1e': 'ctrl-alt-a',
    '\x000': 'ctrl-alt-b',
    '\x00.': 'ctrl-alt-c',
    '\x00 ': 'ctrl-alt-d',
    '\x00\x12': 'ctrl-alt-e',
    '\x00!': 'ctrl-alt-f',
    '\x00"': 'ctrl-alt-g',
    '\x00#': 'ctrl-alt-h',
    '\x00\x17': 'ctrl-alt-i',
    '\x00$': 'ctrl-alt-j',
    '\x00%': 'ctrl-alt-k',
    '\x00&': 'ctrl-alt-l',
    '\x002': 'ctrl-alt-m',
    '\x001': 'ctrl-alt-n',
    '\x00\x18': 'ctrl-alt-o',
    '\x00\x19': 'ctrl-alt-p',
    '\x00\x10': 'ctrl-alt-q',
    '\x00\x13': 'ctrl-alt-r',
    '\x00\x1f': 'ctrl-alt-s',
    '\x00\x14': 'ctrl-alt-t',
    '\x00\x16': 'ctrl-alt-u',
    '\x00/': 'ctrl-alt-v',
    '\x00\x11': 'ctrl-alt-w',
    '\x00-': 'ctrl-alt-x',
    '\x00\x15': 'ctrl-alt-y',
    '\x00,': 'ctrl-alt-z',
    '\x00x': 'ctrl-alt-1',
    '\x00y': 'ctrl-alt-2',
    '\x00z': 'ctrl-alt-3',
    '\x00{': 'ctrl-alt-4',
    '\x00|': 'ctrl-alt-5',
    '\x00}': 'ctrl-alt-6',
    '\x00~': 'ctrl-alt-7',
    '\x00\x7f': 'ctrl-alt-8',
    '\x00\x80': 'ctrl-alt-9',
    '\x00\x81': 'ctrl-alt-0',
    '\x00\x82': 'ctrl-alt-minus',
    '\x00x83': 'ctrl-alt-equals',
    '\x00\x0e': 'ctrl-alt-backspace',
    '\x00h': 'alt-f1',
    '\x00i': 'alt-f2',
    '\x00j': 'alt-f3',
    '\x00k': 'alt-f4',
    '\x00l': 'alt-f5',
    '\x00m': 'alt-f6',
    '\x00n': 'alt-f7',
    '\x00o': 'alt-f8',
    '\x00p': 'alt-f9',
    '\x00q': 'alt-f10',
    '\xe0\x8b': 'alt-f11',
    '\xe0\x8c': 'alt-f12',
    '\x00\x97': 'alt-home',
    '\x00\x9f': 'alt-end',
    '\x00\xa2': 'alt-insert',
    '\x00\xa3': 'alt-delete',
    '\x00\x99': 'alt-page-up',
    '\x00\xa1': 'alt-page-down',
    '\x00\x9b': 'alt-left',
    '\x00\x9d': 'alt-right',
    '\x00\x98': 'alt-up',
    '\x00\xa0': 'alt-down',
    '\x00\x1a': 'ctrl-alt-left-bracket',
    '\x00\x1b': 'ctrl-alt-right-bracket',
    '\x00\'': 'ctrl-alt-semicolon',
    '\x00(': 'ctrl-alt-single-quote',
    '\x00\x1c': 'ctrl-alt-enter',
    '\x005': 'ctrl-alt-slash',
    '\x004': 'ctrl-alt-period',
    '\x003': 'ctrl-alt-comma',
}
windowsCodeToNameMapping.update(commonCodeToNameMapping)

unixCodeToNameMapping = {
    '\x1bOP': 'f1',
    '\x1bOQ': 'f2',
    '\x1bOR': 'f3',
    '\x1bOS': 'f4',
    '\x1b[A': 'up',
    '\x1b[B': 'down',
    '\x1b[C': 'right',
    '\x1b[D': 'left',
    '\x1bOP': 'f1',
    '\x1bOQ': 'f2',
    '\x1bOR': 'f3',
    '\x1bOS': 'f4',
    '\x1bOA': 'up',
    '\x1bOB': 'down',
    '\x1bOC': 'right',
    '\x1bOD': 'left',
    '\x1bOp': 'keypad-0',
    '\x1bOq': 'keypad-1',
    '\x1bOr': 'keypad-2',
    '\x1bOs': 'keypad-3',
    '\x1bOt': 'keypad-4',
    '\x1bOu': 'keypad-5',
    '\x1bOv': 'keypad-6',
    '\x1bOw': 'keypad-7',
    '\x1bOx': 'keypad-8',
    '\x1bOy': 'keypad-9',
    '\x1bOm': 'keypad-minus',
    '\x1bOl': 'keypad-comma',
    '\x1bOn': 'keypad-period',
    '\x1bOM': 'keypad-enter',
    '\x1b[11~': 'f1',
    '\x1b[12~': 'f2',
    '\x1b[13~': 'f3',
    '\x1b[14~': 'f4',
    '\x1b[15~': 'f5',
    '\x1b[17~': 'f6',
    '\x1b[18~': 'f7',
    '\x1b[19~': 'f8',
    '\x1b[20~': 'f9',
    '\x1b[21~': 'f10',
    '\x1b[23~': 'f11',
    '\x1b[24~': 'f12',
    '\x1b[H': 'home',
    '\x1b[F': 'end',
    '\x1b[5': 'page-up',
    '\x1b[6': 'page-down',
    '\x7f': 'backspace',
    '\x1b[2~': 'insert',
    '\x1b[3~': 'delete',
}
unixCodeToNameMapping.update(commonCodeToNameMapping)

windowsPrefixes = set()
for code, key in windowsCodeToNameMapping.items():
    if len(code) > 1:
        for i in range(len(code)):
            windowsPrefixes.add(code[:i])

unixPrefixes = set()
for code, key in unixCodeToNameMapping.items():
    if len(code) > 1:
        for i in range(len(code)):
            unixPrefixes.add(code[:i])


class GetKeyUnix(object):
    def __init__(self):
        try:
            self.__decoded_stream = OSReadWrapper()
        except Exception as err:
            raise BextException('Cannot use unix platform on non-file-like stream')

    def getkey(self, blocking=True):
        buffer = ''
        for c in self.getcharsUnix(blocking):
            buffer += c
            if buffer not in unixPrefixes:
                break

        if buffer == '\x03':
            raise KeyboardInterrupt
        if buffer == '':
            return ''  # In non-blocking mode, return '' if nothing was pressed.
        return unixCodeToNameMapping.get(buffer, buffer)

    def fileno(self):
        return self.__decoded_stream.fileno()

    @contextmanager
    def context(self):
        fd = self.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        try:
            yield
        finally:
            termios.tcsetattr(
                fd, termios.TCSADRAIN, old_settings
            )

    def getchars(self, blocking=True):
        """Get characters on Unix."""
        with self.context():
            if blocking:
                yield self.__decoded_stream.read(1)
            while select.select([self.fileno()], [], [], 0)[0]:
                yield self.__decoded_stream.read(1)


class OSReadWrapper(object):
    def __init__(self):
        self.__decoder = codecs.getincrementaldecoder(sys.stdin.encoding)()

    def fileno(self):
        return sys.stdin.fileno()

    @property
    def buffer(self):
        return sys.stdin.buffer

    def read(self, chars):
        buffer = ''
        while len(buffer) < chars:
            buffer += self.__decoder.decode(os.read(sys.stdin.fileno(), 1))
        return buffer


class GetKeyWindows(object):
    def getkey(self, blocking=True):
        buffer = ''
        for c in self.getchars(blocking):
            buffer += c.decode(encoding=locale.getpreferredencoding())
            if buffer not in windowsPrefixes:
                break

        if buffer == '\x03':
            raise KeyboardInterrupt
        if buffer == '':
            return ''  # In non-blocking mode, return '' if nothing was pressed.
        return windowsCodeToNameMapping.get(buffer, buffer)

    def getchars(self, blocking=True):
        """Get characters on Windows."""

        if blocking:
            yield msvcrt.getch()
        while msvcrt.kbhit():
            yield msvcrt.getch()


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
        raise BextException('x coordinate is negative')
    if y < 0:
        raise BextException('y coordinate is negative')

    width, height = shutil.get_terminal_size()

    if x >= width:
        raise BextException('x coordinate is greater than terminal width ' + str(width))
    if y >= height:
        raise BextException('y coordinate is greater than terminal height ' + str(height))

    sys.stdout.write('\x1b[%d;%dH' % (y + 1, x + 1))


def _goto_win32_api(x, y):
    """Repositions the cursor to the x, y coordinates in the terminal window.

    (0, 0) is the top-left corner coordinate."""
    if x < 0:
        raise BextException('x coordinate is negative')
    if y < 0:
        raise BextException('y coordinate is negative')

    width, height = shutil.get_terminal_size()

    if x >= width:
        raise BextException('x coordinate is greater than terminal width ' + str(width))
    if y >= height:
        raise BextException('y coordinate is greater than terminal height ' + str(height))

    h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleCursorPosition(h, COORD(x, y))


def resize(columns, rows):
    """Resize the terminal window. Returns True if the resize was successful,
    otherwise returns False."""
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
    """Returns the width of the terminal in columns as an int."""
    return shutil.get_terminal_size()[0]


def height():
    """Returns the height of the terminal in rows as an int."""
    return shutil.get_terminal_size()[1]


def clear(mode=2):  # TODO - what does mode mean?
    """Clears the terminal and positions the cursor at the top-left corner."""
    sys.stdout.write(colorama.ansi.CSI + str(mode) + 'J')
    # On macOS and Linux, clearing doesn't reset the cursor back to the top-left
    # corner of the termnal window, so do that here:
    goto(0, 0)


def title(text):
    """Sets the title of the terminal window to `text`."""
    sys.stdout.write(colorama.ansi.OSC + '2;' + text + colorama.ansi.BEL)


def hide():
    """"Hides the cursor."""
    if sys.platform == 'win32':
        # This only works in the Command Prompt and PowerShell, not in other terminal-like environments.
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    else:
        sys.out.write('\033[?25l')
        sys.out.flush()


def show():
    """Shows the cursor after hiding it."""
    if sys.platform == 'win32':
        # This only works in the Command Prompt and PowerShell, not in other terminal-like environments.
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    else:
        sys.out.write('\033[?25h')
        sys.out.flush()


# https://en.wikipedia.org/wiki/Windows_Glyph_List_4
allChrs = {}
allOrds = {}
for _start, _stop in ((0x21, 0x7f), (0xa1, 0x180), (0x192, 0x193), (0x1fa, 0x200), (0x2c6, 0x2c8), (0x2c9, 0x2ca),
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
        for i in range(_start, _stop):
            allChrs[i] = chr(i)
            allOrds[chr(i)] = i


# Figure out which modules to import:
if sys.platform.startswith('cygwin'):
    try:
        import msvcrt
    except ImportError:
        currentPlatform = 'unix'
    else:
        currentPlatform = 'windows'
if sys.platform == 'win32':
    currentPlatform = 'windows'
elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    currentPlatform = 'unix'

# Import the modules for this platform:
if currentPlatform == 'windows':
    import msvcrt, ctypes, locale
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        pass

    COORD._fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    goto = _goto_win32_api
    getKey = GetKeyWindows().getkey
elif currentPlatform == 'unix':
    # macOS and Linux:
    import tty, termios, select, codecs  # Used by getKey()
    goto = _goto_control_code
    getKey = GetKeyUnix().getkey
else:
    raise BextException('Unknown platform:' + sys.platform)

init() # Automatically called on import. Initializes Colorama.
