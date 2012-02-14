import sys
import ply.yacc as yacc
from lexer import tokens
from core import Atom, Keyword, List, Vector, Map

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

def lispparser():
    def p_sexpr_nil(p):
        'sexpr : NIL'
        p[0] = None

    def p_sexpr_atom(p):
        'sexpr : ATOM'
        p[0] = Atom(p[1])

    def p_keyword(p):
        'sexpr : KEYWORD'
        p[0] = Keyword(p[1])

    def p_sexpr_float(p):
        'sexpr : FLOAT'
        p[0] = float(p[1])

    def p_sexpr_integer(p):
        'sexpr : INTEGER'
        p[0] = int(p[1])

    def p_sexpr_seq(p):
        '''
        sexpr : list
              | vector
              | map
        '''
        p[0] = p[1]

    def p_sexprs_sexpr(p):
        'sexprs : sexpr'
        p[0] = p[1]

    def p_sexprs_sexprs_sexpr(p):
        'sexprs : sexprs sexpr'
        #p[0] = ', '.join((p[1], p[2]))
        if type(p[1]) is list:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1], p[2]]

    def p_list(p):
        'list : LPAREN sexprs RPAREN'
        try:
            p[0] = apply(List, p[2])
        except TypeError:
            p[0] = List(p[2])

    def p_empty_list(p):
        'list : LPAREN RPAREN'
        p[0] = List()

    def p_vector(p):
        'vector : LBRACKET sexprs RBRACKET'
        try:
            p[0] = apply(Vector, p[2])
        except TypeError:
            p[0] = Vector(p[2])

    def p_empty_vector(p):
        'vector : LBRACKET RBRACKET'
        p[0] = Vector()

    def p_map(p):
        'map : LBRACE sexpr sexpr RBRACE'
        m = Map()
        m[p[2]] = p[3]
        p[0] = m

    def p_empty_map(p):
        'map : LBRACE RBRACE'
        p[0] = Map()

    def p_error(p):
        if p:
            print(p.lineno, "Syntax error in input at token '%s'" % p.value)
        else:
            print("EOF","Syntax error. No more input.")

    return yacc.yacc(errorlog=LispLogger(sys.stderr)).parse
