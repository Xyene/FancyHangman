import pyglet
import os
import sys

if __name__ == '__main__':
    print "Booting..."

    sys.path.append(os.path.dirname(sys.executable))

    with open("hangman/__main__.py", 'r') as f:
        code = f.read()
        exec code