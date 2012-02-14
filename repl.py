#!/usr/bin/env python

from lexer import lisplexer
from parser import lispparser
from core import evaluate, tostring, Scope
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

parse = lispparser()
lexer = lisplexer()

if __name__ == "__main__":
    global_scope = Scope()
    scopechain = [global_scope]
    while True:
        try:
            txt = raw_input("pylisp> ")
            if re.search('^\s*$', txt):
                continue
            else:
                print(tostring(evaluate(parse(txt), scopechain)))
        except (EOFError, KeyboardInterrupt):
            print
            break
        except Exception, e:
            print e
