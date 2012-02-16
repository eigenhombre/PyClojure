import ply.lex as lex

class PyClojureLex(object):
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    reserved = {'nil': 'NIL'}

    tokens = ['ATOM', 'KEYWORD',
              'NUMBER', 'READMACRO',
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

    def t_NUMBER(self, t):
        r'[+-]?((\d+(\.\d+)?([eE][+-]?\d+)?)|(\.\d+([eE][+-]?\d+)?))'
        val = t.value
        if '.' in val or 'e' in val.lower():
            t.type = 'FLOAT'
        else:
            t.type = 'INTEGER'
        return t

    def t_ATOM(self, t):
        r'[\*\+\!\-\_a-zA-Z_-]+'
        t.type = self.reserved.get(t.value, 'ATOM')
        return t

    def t_READMACRO(self, t):
        r'[@\'#^`\\.][\*\+\!\-\_a-zA-Z_-]+'
        # Just the standard atom regex will all the possible reader
        # chars prepended to it.
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
