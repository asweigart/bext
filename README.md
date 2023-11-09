Bext
======

A cross-platform Python 2/3 module for colorful, boring, text-based terminal programs.

Basically, use Bext if you want to move the cursor around the terminal window and have colorful text, like some kind of limited curses module (but it works on Windows also.)

Bext does not currently work in the new Windows Terminal. It does work in the older Command Prompt.

Note: Currently something in Colorama 0.4.6 causes Bext to fail. Please use 0.4.5 or earlier.

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

* ``resize(columns, rows)``

Resizes the terminal window to the given number of columns and rows. Returns `True` if the resize was a success and `False` if not. Note that on Ubuntu Linux, this function doesn't work if the Terminal window is maximized. On Windows, if the Command Prompt is maximized the window won't change size but the screen buffer size will be resized. This function is not very reliable.

* ``clear()``

Erase all the text on the screen, paint the entire terminal to the background color, and moves the cursor to (0, 0) at the top-left corner of the screen.

* ``clear_line()``

Erases the line where the cursor is located.

* ``goto(x, y)``

Move the cursor to x, y coordinates on the screen. (0, 0) is the top-left corner of the screen.

* ``title(text)``

Sets the title of the terminal window to `text`.

* ``hide_cursor()``

Hides the cursor.

* ``show_cursor()``

Shows the cursor after hiding it.

* ``get_key(blocking=True)``

Waits until the user presses a single key on the keyboard, then returns that key as a string. If `blocking` is `False`, the function returns immediately (returning `None` if no key has been pressed.)

Example
-------

```python

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

```

Contribute
----------

If you'd like to contribute to Bext, check out https://github.com/asweigart/bext

Support
-------

If you find this project helpful and would like to support its development, [consider donating to its creator on Patreon](https://www.patreon.com/AlSweigart).
