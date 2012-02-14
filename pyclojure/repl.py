#!/usr/bin/env python

import re
from pyclojure.lexer import lisplexer
from pyclojure.parser import lispparser
from pyclojure.core import evaluate, tostring, Scope


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
