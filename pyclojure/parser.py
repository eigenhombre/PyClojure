import sys
import ply.yacc as yacc
from pyclojure.lexer import PyClojureLex
from pyclojure.core import Atom, Keyword, List, Vector, Map

# BNF grammar for 'lisp'
# sexpr : atom
#       | keyword
#       | float
#       | integer
#       | list
#       | vector
#       | map
#       | nil
# sexprs : sexpr
#        | sexprs sexpr
# list : ( sexprs )
#      | ( )

_quiet = True

class LispLogger(yacc.PlyLogger):
    def debug(self, *args, **kwargs):
        if not _quiet:
            super(type(self), self).debug(*args, **kwargs)

def make_map(args):
    m = Map()
    kvlist = [(args[i], args[i+1]) for i in range(0, len(args), 2)]
    for k, v in kvlist:
        m[k] = v
    return m

class PyClojureParse(object):
    def build(self):
        return yacc.yacc(module=self, errorlog=LispLogger(sys.stderr))

    tokens = PyClojureLex.tokens
    tokens.remove('NUMBER')
    tokens.extend(('FLOAT', 'INTEGER'))

    def p_sexpr_nil(self, p):
        'sexpr : NIL'
        p[0] = None

    def p_sexpr_atom(self, p):
        'sexpr : ATOM'
        p[0] = Atom(p[1])

    def p_keyword(self, p):
        'sexpr : KEYWORD'
        p[0] = Keyword(p[1])

    def p_sexpr_float(self, p):
        'sexpr : FLOAT'
        p[0] = float(p[1])

    def p_sexpr_integer(self, p):
        'sexpr : INTEGER'
        p[0] = int(p[1])

    def p_sexpr_seq(self, p):
        '''
        sexpr : list
              | vector
              | map
        '''
        p[0] = p[1]

    def p_sexprs_sexpr(self, p):
        'sexprs : sexpr'
        p[0] = p[1]

    def p_sexprs_sexprs_sexpr(self, p):
        'sexprs : sexprs sexpr'
        #p[0] = ', '.join((p[1], p[2]))
        if type(p[1]) is list:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1], p[2]]

    def p_list(self, p):
        'list : LPAREN sexprs RPAREN'
        try:
            p[0] = apply(List, p[2])
        except TypeError:
            p[0] = List(p[2])

    def p_empty_list(self, p):
        'list : LPAREN RPAREN'
        p[0] = List()

    def p_vector(self, p):
        'vector : LBRACKET sexprs RBRACKET'
        try:
            p[0] = apply(Vector, p[2])
        except TypeError:
            p[0] = Vector(p[2])

    def p_empty_vector(self, p):
        'vector : LBRACKET RBRACKET'
        p[0] = Vector()

    def p_map(self, p):
        'map : LBRACE sexpr sexpr RBRACE'
        p[0] = make_map(p[2])

    def p_empty_map(self, p):
        'map : LBRACE RBRACE'
        p[0] = Map()

    def p_error(self, p):
        if p:
            print(p.lineno, "Syntax error in input at token '%s'" % p.value)
        else:
            print("EOF","Syntax error. No more input.")
