import ply.lex as lex

class PyClojureLex(object):
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    reserved = {'nil': 'NIL'}

    tokens = ['ATOM', 'KEYWORD',
              'FLOAT', 'INTEGER',
              'LBRACKET', 'RBRACKET',
              'LBRACE', 'RBRACE',
              'LPAREN', 'RPAREN'] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_ignore = ' ,\t\r'
    t_ignore_COMMENT = r'\;.*'

    def t_KEYWORD(self, t):
        r'\:[a-zA-Z_-]+'
        t.value = t.value[1:]
        return t

    def t_FLOAT(self, t):
        r'[-+]?([0-9]*\.[0-9]+|[0-9]+\.)'
        return t

    def t_INTEGER(self, t):
        r'[0-9]+'
        return t

    def t_ATOM(self, t):
        r'[\*\+\!\-\_a-zA-Z_-]+'
        t.type = self.reserved.get(t.value, 'ATOM')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
