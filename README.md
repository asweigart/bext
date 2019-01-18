Bext
======

A cross-platform Python 2/3 module for colorful, boring, text-based terminal programs.

Basically, use Bext if you want to move the cursor around the terminal window and have colorful text, like some kind of limited curses module (but it works on Windows also.)

Installation
------------

To install with pip, run:

    pip install bext

Functions
---------

* ``fg(color)``

Sets the foreground color, that is, the color of the text. The color is a string of one of the following colors: black, red, green, yellow, blue, purple, cyan, white, reset, random.

* ``bg(color)``

Sets the background color, that is, the color of the cell behind the text characters. You "paint" a cell with the background color by printing a space character.

* ``size()``

Returns a tuple of the (width, height) of the current terminal.

* ``clear()``

Erase all the text on the screen, paint the entire terminal to the background color, and

* ``goto(x, y)``

Move the cursor to x, y coordinates on the screen. (0, 0) is the top-left corner of the screen.


Example
-------

    import bext, random

    width, height = bext.size()

    try:
        while True:
            bext.fg('random')
            bext.bg('random')
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if x == width -1 and y == height - 1:
                continue # Windows has weird behavior where a character at the end of the row always moves the cursor to the next row.
            bext.goto(x, y)
            print('*', end='')
    except KeyboardInterrupt:
        pass

Contribute
----------

If you'd like to contribute to Bext, check out https://github.com/asweigart/bext
