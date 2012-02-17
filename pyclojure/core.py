import operator
from funktown import ImmutableDict, ImmutableVector


class ComparableExpr(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not (self == other)


class Map(ComparableExpr, ImmutableDict):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            ImmutableDict.__init__(self, args[0])
        else:
            ImmutableDict.__init__(self, kwargs)

    def __eq__(self, other):
        try:
            my_keys = sorted(self.keys())
            their_keys = sorted(other.keys())
            for mine, theirs in zip(my_keys, their_keys):
                if mine != theirs:
                    return False
                if self[mine] != other[theirs]:
                    return False
        except:
            return False
        else:
            return True

    def __repr__(self):
        return 'MAP(%s)' % (dict(self))

class Atom(ComparableExpr):
    def __init__(self, name=None, value=None):
        self.__name = name

    def name(self):
        return self.__name

    def __repr__(self):
        return "ATOM(%s)" % (self.__name)


class ComparableIter(ComparableExpr):
    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False
            for a, b in zip(self, other):
                if a != b:
                    return False
        except:
            return False
        else:
            return True


class List(ComparableIter, list):
    def __init__(self, *args):
        for arg in args:
            self.append(arg)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__.upper(),
                           ','.join([str(el) for el in self]))


class Vector(ComparableIter, ImmutableVector):
    def __init__(self, *args):
        ImmutableVector.__init__(self, args)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__.upper(),
                           ','.join([str(el) for el in self]))


class Keyword(ComparableExpr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return ":"+self.name


class Function(ComparableExpr):
    pass


class Scope(dict):
    pass


class GlobalScope(Scope):
    def __init__(self, *args, **kwargs):
        Scope.__init__(self, *args, **kwargs)
        # Get all builtin python functions
        python_callables = [(name, obj) for name, obj\
                                in __builtins__.items() if\
                                callable(obj)]
        self.update(python_callables)

        # These functions take a variable number of arguments
        variadic_operators = {'+': ('add', 0),
                              '-': ('sub', 0),
                              '*': ('mul', 1),
                              '/': ('div', 1)}
        def variadic_generator(fname, default):
            func = getattr(operator, fname)
            ret = (lambda *args: reduce(func, args) if args else default)
            # For string representation; otherwise just get 'lambda':
            ret.__name__ = fname
            return ret

        for name, info in variadic_operators.items():
            self[name] = variadic_generator(*info)

        non_variadic_operators = {
            '!': operator.inv,
            '==': operator.eq,
            }
        self.update((name, func) for name, func in\
                        non_variadic_operators.items())


class UnknownVariable(Exception):
    pass


BUILTIN_FUNCTIONS = {}

def register_builtin(name):
    """
    A decorator that registers built in functions.

    @register_builtin("def")
    def def(args, scopes):
        implementation here
    """
    def inner(func):
        BUILTIN_FUNCTIONS[name] = func
        return func
    return inner

@register_builtin("def")
def def_(args, scopes):
    if len(args) != 2:
        raise TypeError("def takes two arguments")
    atom, rhs = args[0:2]
    if type(atom) is not Atom:
        raise TypeError("First argument to def must be atom")
    scopes[-1][atom.name()] = evaluate(rhs, scopes)


def find_in_scopechain(scopes, name):
    for scope in reversed(scopes):
        try:
            return scope[name]
        except KeyError:
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
    elif x.__class__.__name__ in ['function', 'builtin_function_or_method']:
        return str(x)
    elif type(x) is List:
        inner = ' '.join([tostring(x) for x in x])
        return '(%s)' % inner
    elif type(x) is Vector:
        inner = ' '.join([tostring(x) for x in x])
        return '[%s]' % inner
    elif type(x) is Map:
        inner = ', '.join(['%s %s' % (k, v) for k,v in x.items()])
        return '{%s}' % inner
    else:
        raise TypeError('%s is unknown!' % x)


def evaluate(x, scopes):
    if type(x) in (int, float):
        return x
    elif type(x) is Atom:
        val = find_in_scopechain(scopes, x.name())
        if not val:
            raise UnknownVariable("Unknown variable: %s" % x.name())
        else:
            return val
    elif type(x) is Keyword:
        return x
    elif type(x) is Vector:
        return apply(Vector, [evaluate(el, scopes) for el in x])
    elif type(x) is Map:
        return Map(dict([(evaluate(k, scopes), evaluate(v, scopes))
                         for k, v in x.items()]))
    elif type(x) is List:
        contents = x
        return eval_list(contents, scopes)
    return x


def eval_list(contents, scopes):
    if len(contents) == 0:
        return List()  # ()
    first = contents[0]
    rest = contents[1:]
    if type(first) is Map:
        if len(rest) != 1:
            raise TypeError("Map lookup takes one argument")
        return evaluate(first, scopes)[evaluate(rest[0], scopes)]
    elif type(first) is Atom:
        name = first.name()
        if name in BUILTIN_FUNCTIONS:
            func = BUILTIN_FUNCTIONS[name]
            return func(rest, scopes)
        else:
            val = find_in_scopechain(scopes, name)
            if not val:
                raise UnknownVariable("Function %s is unknown" % name)
            if callable(val):
                args = map((lambda obj: evaluate(obj, scopes)), rest)
                return val(*args)
            else:
                raise TypeError("%s is not callable" % name)
