import ply.yacc as yacc
from lisp_lex import tokens
from lisp_core import Atom, List

# BNF grammar for 'lisp'
# sexpr : atom
#       | integer
#       | list
#       | nil
# sexprs : sexpr
#        | sexprs sexpr
# list : ( sexprs )
#      | ( )

def lispparser():
    def p_sexpr_nil(p):
        'sexpr : NIL'
        p[0] = None

    def p_sexpr_atom(p):
        'sexpr : ATOM'
        p[0] = Atom(p[1])

    def p_sexpr_integer(p):
        'sexpr : INTEGER'
        p[0] = int(p[1])

    def p_sexpr_list(p):
        'sexpr : list'
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

    return yacc.yacc().parse
