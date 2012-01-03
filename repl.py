#!/usr/bin/env python

from lisp_lex import tokens, lisplexer
from lisp_yacc import lispparser
from lisp_core import evaluate, tostring, Scope
import re


parse = lispparser()
lexer = lisplexer()

if __name__ == "__main__":
    globals = Scope()
    scopechain = [globals]
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
