from distutils.core import setup
import py2exe
from glob import glob
import sys
import os

sys.argv.append("py2exe")

data = []

parent = os.path.abspath(__file__ + "/../")
join = os.path.join

resources = [("hangman", ["*.py", "*.txt"])]

for res in resources:
    dir, patterns = res
    for pattern in patterns:
        for file in glob(join(dir, pattern)):
            print "Packaging", join(parent, file), "->", dir
            data.append((dir, [join(parent, file)]))

setup(
    console=["bootloader.py"],
    data_files=data,
    options={
        "py2exe": {
            "unbuffered": True,
            "optimize": 2,
            "dist_dir": "bin"
        }
    },
    requires=['pyglet']
)

os.chdir("bin")
try:
    os.remove("Hangman.exe")
except:
    pass
os.rename("bootloader.exe", "Hangman.exe")