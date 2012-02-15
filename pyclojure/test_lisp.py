from pyclojure.lexer import PyClojureLex  # Need tokens for parser
from pyclojure.parser import PyClojureParse
from pyclojure.core import (Atom, Keyword, Vector, List, Map, Scope, evaluate,
                            tostring, UnknownVariable, GlobalScope)


def test_lexer():
    lexer = PyClojureLex().build()
    lexer.input("""(a
                      (nested) list (of 534 atoms [and :symbols]
                          (and lists)))  ;; with comments
                """)
    assert 20 == len([tok for tok in lexer])
    lexer.input("")
    assert [tok for tok in lexer] == []


def test_parser():
    parse = PyClojureParse().build().parse
    assert parse("an_atom") == Atom('an_atom')
    assert parse("(simple_list)") == List(Atom('simple_list'))
    assert parse('(two elements)') == List(Atom('two'),
                                                  Atom('elements'))
    assert (parse("(three element list)") ==
            List(Atom('three'), Atom('element'), Atom('list')))
    assert parse('666') == 666
    assert (parse('(a (nested (list)))') ==
            List(Atom('a'), List(Atom('nested'), List(Atom('list')))))
    assert parse('()') == List()


def test_core():
    Atom()
    Atom('a')
    Atom(name='a', value=6)
    List()
    List(Atom('car'))
    List(Atom('car'), Atom('cadr'), 666)
    List(List())
    List(List('car'))
    Vector()
    Vector(1, 2, 3)
    Keyword("a")
    assert Atom() == Atom()
    assert List() == List()
    assert List(1) == List(1)
    assert List(2) != List(1)
    assert List(1, 2) != List(2, 1)
    assert List(1, 2) == List(1, 2)
    assert List(Atom()) == List(Atom())
    assert List(Atom('a')) == List(Atom('a'))
    assert List(Atom('b')) != List(Atom('a'))
    assert Vector(1, 2) != Vector(2, 1)
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(1, 2) != List(1, 2)
    assert Keyword("a") == Keyword("a")
    assert Keyword("a") != Keyword("b")
    Map()
    Map(x=1)
    assert Map(x=1).keys() == ['x']
    assert Map(x=1) == Map(x=1)
    assert Map(x=1) != Map(x=2)
    assert Map(x=1) != Map(x=1, a=3)
    assert Map(x=1)["x"] == 1
    Map()["1"] = 2


def test_eval():
    parse = PyClojureParse().build().parse
    scopechain = [GlobalScope()]
    def evalparse(x):
        return evaluate(parse(x), scopechain)
    assert evalparse("666") == 666
    assert evalparse("6.66") == 6.66
    assert evalparse("nil") == None
    assert evalparse("()") == List()
    assert evalparse("[]") == Vector()
    assert evalparse("[1 2 3]") == Vector(1, 2, 3)
    assert evalparse("{}") == Map()
    m = Map()
    m[1] = 2
    assert evalparse("{1 2}") == m
    m[3] = 4
    assert evalparse("{1 2, 3 4}") == m

    try:
        evalparse("a")
        assert False, "UnknownVariable exception not raised!"
    except UnknownVariable:
        pass
    try:
        evalparse("(x)")
        assert False, "UnknownVariable exception not raised!"
    except UnknownVariable:
        pass
    scopechain[-1]["a"] = 777
    assert evalparse("a") == 777
    assert evalparse("a") == 777
    evalparse("(def a 666)")
    assert evalparse("a") == 666
    assert evalparse("[1 a]") == Vector(1, 666)
    assert evalparse(":a") == Keyword("a")
    assert evalparse("(+ 2 2)") == 4
    assert evalparse("(+)") == 0
    assert evalparse("(+ 1 2 3 4)") == 10
    assert evalparse("(*)") == 1
    assert evalparse("(* 1 2 3 4 5)") == 120
    assert evalparse("(+ 2 (+ 2 3))") == 7
    assert evalparse("{}") == Map()
    assert evalparse("{1 2}") == Map({1: 2})
    assert evalparse("({1 2} 1)") == 2
    assert evalparse("({a 1} 666)") == 1
    assert evalparse("({666 1} a)") == 1
    assert evalparse("({a 2 3 a} a)") == 2
    assert evalparse("({a 2 3 a} 3)") == 666

def test_function_calling():
    parse = PyClojureParse().build().parse
    scopechain = [GlobalScope()]
    def evalparse(x):
        return evaluate(parse(x), scopechain)
    # Test builtin python function calling
    assert evalparse("(abs (- 0 100))") == 100
    assert evalparse("(round 3.3)") == 3.0


def test_to_string():
    parse = PyClojureParse().build().parse
    assert tostring(parse("nil")) =="nil"
    assert tostring(parse("666")) =="666"
    assert tostring(parse("6.66")) == "6.66"
    assert tostring(parse("666e-3")) == "6.66"
    assert tostring(parse("-666")) =="-666"
    assert tostring(parse("-6.66")) == "-6.66"
    assert tostring(parse("-666e-3")) == "-6.66"
    assert tostring(parse("()")) == "()"
    assert tostring(parse("(a)")) == "(a)"
    assert tostring(parse("(a b)")) == "(a b)"
    assert tostring(parse("(a (b c))")) == "(a (b c))"
    assert tostring(parse("[]")) == "[]"
    assert tostring(parse(":a")) == ":a"
    assert tostring(parse("{}")) == "{}"
    assert tostring(parse("{1 2}")) == "{1 2}"
    assert tostring(parse("{1 2 3 4}")) == "{1 2, 3 4}"


def test_scope():
    s = Scope()
    s["a"] = 666
