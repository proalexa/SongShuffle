import sys
from cx_Freeze import setup, Executable


options = {"packages": ["os","youtube_dl","pafy","vlc","sys","random","bs4","time","urllib"], "excludes": ["tkinter"]}

base = None

setup(  name = "ss",
        version = "0.1",
        description = "Song Shuffler",
        options = {"build_exe": options},
        executables = [Executable("main.py", base=base)])