#!/usr/bin/python
# Hangman
# A fun command-line console game.
# Tudor Brindus
# 2013-11-04
# --------------------------------
import os
import pyglet
from hangman.loading import Applet
from hangman import hangman

try:
    from hangman.conex import *
    WIN = True
except:
    WIN = False

PBUFFER_HEIGHT = 50
PBUFFER_WIDTH = 80
DEBUG = False


def main():
    '''
        This game does not play nice with the console.
        Some may say it violates the console.
        That the console is left lifeless.
        A fragment of what it once was.
        That the console will be schkruud by He Who's Name Cannot Be Expressed in the Basic Multilingual Plane -
            he comes.
        Fonts, colour and screen buffer are treated equally by this program
            as meaningless casualties.
        The ctype violation of fonts, colour et al. will destroy your mind like so much watery putty.

        You have been warned.

        TODO: make the above text rhyme
    '''
    os.system("title Hangman")
    print "Initializing..."
    if not DEBUG: # You have no idea how painful a 10-second loading screen is while debuggins
        # We only support console extensions on Windows
        if WIN:
            font = get_font() # Obtain the raster font
            # We make each character 8x8 px, so that they collectively line up like pixels would.
            # We save the initial size to restore later.
            _x, _y = font.dwFontSize.X, font.dwFontSize.Y
            font.dwFontSize.X = 8
            font.dwFontSize.Y = 8
            set_font(font)

        # Initialize a window to act as a makeshift pbuffer; not like anyone should see the title anyways.
        window = Applet(width=PBUFFER_WIDTH, height=PBUFFER_HEIGHT, caption="3DASCII$PBuffer", resizable=True, vsync=0)
        window.set_visible(False)
        pyglet.app.run()

        if WIN:
            # Revert font size
            font.dwFontSize.X = _x
            font.dwFontSize.Y = _y
            set_font(font)

    # Let the game begin!
    hangman.main()


if __name__ == '__main__':
    main()