import sys
#from distutils.core import setup
from cx_Freeze import setup, Executable
from starsbridge import __version__

base = None

# Comment if console application
#if sys.platform == 'win32' : base = 'Win32GUI'

# define python filename to exeutable
exe = Executable(script='starsbridge.py', base=base)

# Setup
setup(
    name = 'starsbridge',
    version = __version__,
    description = 'stars bridge',
    executables = [exe],
)
