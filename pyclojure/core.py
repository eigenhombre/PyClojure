import operator


class ComparableExpr(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)


class Map(ComparableExpr):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            self.__dict = args[0]
        else:
            self.__dict = kwargs

    def __getitem__(self, name):
        return self.__dict[name]

    def __setitem__(self, name, value):
        self.__dict[name] = value

    def __repr__(self):
        return 'MAP(%s)' % (self.__dict)

    def items(self):
        return self.__dict.items()

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

class Atom(ComparableExpr):
    def __init__(self, name=None, value=None):
        self.__name = name

    def name(self):
        return self.__name

    def __repr__(self):
        return "ATOM(%s)" % (self.__name)


class ComparableList(ComparableExpr):
    def __init__(self, *args):
        self.__contents = []
        for arg in args:
            self.__contents.append(arg)

    def contents(self):
        return self.__contents

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__.upper(),
                           ','.join([str(el) for el in self.__contents]))


class List(ComparableList):
    pass


class Vector(ComparableList):
    pass


class Keyword(ComparableExpr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return ":"+self.name


class Function(ComparableExpr):
    pass


class PythonFunction(Function):
    def __init__(self, func):
        self.func = func

    def call(self, args):
        return self.func(*args)

    def __repr__(self):
        return "PYTHONFUNCTION(%s)" % self.func.__name__


class Scope(dict):
    pass


class GlobalScope(Scope):
    def __init__(self, *args, **kwargs):
        Scope.__init__(self, *args, **kwargs)
        # Get all builtin python functions
        python_functions = [(name, PythonFunction(obj)) for name, obj\
                                in __builtins__.items() if\
                                type(abs) == type(obj)]
        self.update(python_functions)

        operators = {'+': 'add',
                     '-': 'sub',
                     '*': 'mul',
                     '/': 'div',
                     '!': 'inv',
                     '==': 'eq',
                     }
        operator_funcs = [(symbol, PythonFunction(getattr(operator, name))) for\
                              symbol, name in operators.items()]
        self.update(operator_funcs)


class UnknownVariable(Exception):
    pass


class TypeError(Exception):
    pass


def find_in_scopechain(scopes, name):
    for scope in reversed(scopes):
        try:
            return scope[name]
        except:
            pass


def tostring(x):
    if x is None:
        return 'nil'
    elif type(x) in (int, float):
        return str(x)
    elif type(x) is Atom:
        return x.name()
    elif type(x) is Keyword:
        return ":"+x.name
    elif type(x) is List:
        inner = ' '.join([tostring(x) for x in x.contents()])
        return '(%s)' % inner
    elif type(x) is Vector:
        inner = ' '.join([tostring(x) for x in x.contents()])
        return '[%s]' % inner
    elif type(x) is Map:
        inner = ', '.join(['%s %s' % (k, v) for k,v in x.items()])
        return '{%s}' % inner
    else:
        raise TypeError('%s is unknown!' % x)


def plus(args=()):
    return reduce(operator.add, args, 0)


def times(args=()):
    return reduce(operator.mul, args, 1)


def evaluate(x, scopes):
    if type(x) in (int, float):
        return x
    elif type(x) is Atom:
        val = find_in_scopechain(scopes, x.name())
        if not val:
            raise UnknownVariable("Unknown variable: %s" % x.name())
    elif type(x) is Keyword:
        return x
    elif type(x) is Vector:
        return apply(Vector, [evaluate(el, scopes) for el in x.contents()])
    elif type(x) is Map:
        return Map(dict([(evaluate(k, scopes), evaluate(v, scopes))
                         for k, v in x.items()]))
    elif type(x) is List:
        contents = x.contents()
        if len(contents) == 0:
            return x  # ()
        first = contents[0]
        if type(first) is Atom:
            name = first.name()
            if name == "def":
                atom, rhs = contents[1:3]
                if type(atom) is not Atom:
                    raise TypeError("%s is not the name of an atom!" %
                                    tostring(atom))
                scopes[-1][atom.name()] = evaluate(rhs, scopes)
                return atom
            elif find_in_scopechain(scopes, name):
                val = find_in_scopechain(scopes, name)
                if issubclass(type(val), Function):
                    args = map((lambda obj: evaluate(obj, scopes)),
                               contents[1:])
                    return val.call(args)
                else:
                    raise TypeError("%s is not callable" % tostring(val))
            else:
                raise UnknownVariable("Function %s is unknown!" % name)
        elif type(first) is Map:
            return evaluate(first, scopes)[evaluate(contents[1], scopes)]
        else:
            raise SyntaxError("%s is not a function or special form!"
                              % first)
    return x
