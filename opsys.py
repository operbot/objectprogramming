#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0209


"runtime"


import importlib
import readline
import rlcompleter
import sys
import termios
import time
import traceback


from op.object import printable
from op.handler import Command, Event, Handler, scan


NAME = "opb"


class Console(Handler):


    def handle(self, event):
        Command.handle(event)
        event.wait()

    def poll(self):
        event = Event()
        event.txt = input("> ")
        event.orig = repr(self)
        return event

    def raw(self, txt):
        print(txt)


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def banner(cfg):
    print(
          "%s started at %s %s" % (
                                   NAME.upper(),
                                   time.ctime(time.time()).replace("  ", " "),
                                   printable(cfg, "debug,verbose")
                                  )
         )


def importer(pname, mname, path):
    mod = None
    spec = importlib.util.spec_from_file_location(mname, path)
    if spec:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scan(mod)
    return mod


def init(pname, mname, path=None):
    mod = importer(pname, mname, path)
    if "init" in dir(mod):
        mod.init()


def print_exc(ex):
    traceback.print_exception(type(ex), ex, ex.__traceback__)


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    readline.redisplay()
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
        for evt in Command.errors:
             print_exc(evt.__exc__)
