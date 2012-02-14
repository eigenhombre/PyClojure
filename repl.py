#!/usr/bin/env python

from lexer import PyClojureLex
from parser import PyClojureParse
from core import evaluate, tostring, GlobalScope
import re

try:
    import readline
except ImportError:
    pass
else:
    import os
    histfile = os.path.join(os.path.expanduser("~"), ".pyclojurehist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        # Pass here as there isn't any history file, so one will be
        # written by atexit
        pass
    import atexit
    atexit.register(readline.write_history_file, histfile)

lexer = PyClojureLex().build()
parser = PyClojureParse().build()

if __name__ == "__main__":
    global_scope = GlobalScope()
    scopechain = [global_scope]
    while True:
        try:
            txt = raw_input("pylisp> ")
            if re.search('^\s*$', txt):
                continue
            else:
                print(tostring(evaluate(
                            parser.parse(txt, lexer=lexer), scopechain)))
        except (EOFError, KeyboardInterrupt):
            print
            break
        except Exception, e:
            print e
