import ctypes
from ctypes.wintypes import *
from ctypes import *

# See docs on SetConsoleTextAttribute: http://msdn.microsoft.com/en-us/library/windows/desktop/ms686047%28v=vs.85%29.aspx
# Standard colours
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_RED = 0x0004
FOREGROUND_INTENSITY = 0x0008
BACKGROUND_BLUE = 0x0010
BACKGROUND_GREEN = 0x0020
BACKGROUND_RED = 0x0040
BACKGROUND_INTENSITY = 0x0080
# Composite colours
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
FOREGROUND_WHITE = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE
BACKGROUND_YELLOW = BACKGROUND_RED | BACKGROUND_GREEN
BACKGROUND_WHITE = BACKGROUND_RED | BACKGROUND_GREEN | BACKGROUND_BLUE

_STDIO_HANDLE = ctypes.windll.kernel32.GetStdHandle(-11)
_WriteFile = ctypes.windll.kernel32.WriteFile
_SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute

# We buffer our text: prevents unneeded write operations, saving a lot of processing time
_buf = []
_dw = DWORD()
_color = 0


def flushc():
    text = ''.join(_buf)
    if _WriteFile(_STDIO_HANDLE, text, len(text), byref(_dw), None) == 0:
        print "StdIO write failed with %s." % ctypes.windll.kernel32.GetLastError()
    del _buf[:]

def printc(color, text):
    global _color
    if _color != color:
        flushc()
        _SetConsoleTextAttribute(_STDIO_HANDLE, color)
        _color = color
    _buf.append(text)


def colorc(color):
    global _color
    if _color != color:
        flushc()
        _SetConsoleTextAttribute(_STDIO_HANDLE, color)
        _color = color

def cursor_pos(x, y):
    ctypes.windll.kernel32.SetConsoleCursorPosition(_STDIO_HANDLE, _COORD(x, y))

# Font methods adapted from http://stackoverflow.com/a/13940780
class CONSOLE_FONT_INFOEX(Structure):
    _fields_ = [("cbSize", c_ulong),
                ("nFont", c_ulong),
                ("dwFontSize", _COORD),
                ("FontFamily", c_uint),
                ("FontWeight", c_uint),
                ("FaceName", c_wchar * 32)]

def set_font(font):
    if not ctypes.windll.kernel32.SetCurrentConsoleFontEx(_STDIO_HANDLE, c_long(False), pointer(font)):
        print "Failed to set font."


def get_font():
    struct = CONSOLE_FONT_INFOEX()
    struct.cbSize = sizeof(CONSOLE_FONT_INFOEX)
    if not ctypes.windll.kernel32.GetCurrentConsoleFontEx(_STDIO_HANDLE, c_long(False), pointer(struct)):
        print "Failed to fetch font."
    return struct