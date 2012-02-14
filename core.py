import operator


class ComparableExpr(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)


class Map(ComparableExpr):
    def __init__(self, **kwargs):
        self.__dict = kwargs

    def __getitem__(self, name):
        return self.__dict[name]

    def __setitem__(self, name, value):
        self.__dict[name] = value

    def __repr__(self):
        return 'MAP(%s)' % (self.__dict)

    def items(self):
        return self.__dict.items()


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


class Scope(dict):
    pass


class UnknownVariable(Exception):
    pass


def find_in_scopechain(scopes, name):
    for scope in reversed(scopes):
        try:
            return scope[name]
        except:
            pass
    raise UnknownVariable("Unknown variable: %s" % name)


def tostring(x):
    if x is None:
        return 'nil'
    elif type(x) is int:
        return str(x)
    elif type(x) is float:
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
        inner = ','.join(['%s %s' % (k, v) for k,v in x.items()])
        return '{%s}' % inner
    else:
        raise TypeError('%s is unknown!' % x)


def plus(args=[]):
    return reduce(operator.add, args, 0)


def times(args=[]):
    return reduce(operator.mul, args, 1)


builtins = {'+': plus,
            '*': times}


def evaluate(x, scopes):
    if type(x) is int:
        return x
    elif type(x) is Atom:
        return find_in_scopechain(scopes, x.name())
    elif type(x) is Keyword:
        return x
    elif type(x) is Vector:
        return apply(Vector, [evaluate(el, scopes) for el in x.contents()])
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
            elif name in builtins:
                return builtins[name]([evaluate(x, scopes)
                                       for x in contents[1:]])
    return x
