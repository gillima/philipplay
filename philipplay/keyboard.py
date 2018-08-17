"""
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import os

import time

if os.name == 'nt':  # Windows
    # noinspection PyUnresolvedReferences
    import msvcrt
else:  # Posix (Linux, OS X)
    import sys
    import termios
    import atexit
    from select import select


# noinspection PyMethodMayBeStatic
class Keyboard:
    def __init__(self):
        """Creates a KBHit object that you can call to do various keyboard things."""
        if os.name == 'nt':
            pass
        else:
            try:
                # Save the terminal settings
                self.fd = sys.stdin.fileno()
                self.new_term = termios.tcgetattr(self.fd)
                self.old_term = termios.tcgetattr(self.fd)

                # New terminal setting unbuffered
                self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
                termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

                # Support normal-terminal reset at exit
                atexit.register(self.set_normal_term)
            except:
                self.old_term = []

    def set_normal_term(self):
        """Resets to normal terminal.  On Windows this is a no-op."""
        if os.name == 'nt':
            pass
        elif self.old_term:
            try:
                termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
            except:
                pass

    def get_char(self):
        """
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        if os.name == 'nt':
            raw_char = msvcrt.get_char().decode('utf-8')
        else:
            raw_char = sys.stdin.read(1)
        return ord(raw_char.strip().lower())

    def get_arrow(self):
        """
        Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        """
        if os.name == 'nt':
            msvcrt.get_char()  # skip 0xE0
            c = msvcrt.get_char()
            vals = [72, 77, 80, 75]
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        return vals.index(ord(c.decode('utf-8')))

    def key_pressed(self):
        """Returns True if keyboard character was hit, False otherwise."""
        if os.name == 'nt':
            return msvcrt.key_pressed()
        elif self.old_term:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []
        else:
            return False
