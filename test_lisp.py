from lexer import lisplexer  # Need tokens for parser
from parser import lispparser
from core import (Atom, Keyword, Vector, List, Scope, evaluate, tostring,
                  UnknownVariable, builtins)


def test_builtins():
    assert builtins['+']() == 0
    assert builtins['+']([2, 2]) == 4
    assert builtins['*']() == 1
    assert builtins['*']([1, 2, 3]) == 6


def test_lexer():
    lexer = lisplexer()
    lexer.input("""(a 
                      (nested) list (of 534 atoms [and :symbols]
                          (and lists)))  ;; with comments
                """)
    assert 20 == len([tok for tok in lexer])
    lexer.input("")
    assert [tok for tok in lexer] == []


def test_parser():
    parse = lispparser()
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


def test_eval():
    parse = lispparser()
    scopechain = [Scope()]
    def evalparse(x):
        return evaluate(parse(x), scopechain)
    assert evalparse("666") == 666
    assert evalparse("666") == 666
    assert evalparse("nil") == None
    assert evalparse("()") == List()
    assert evalparse("[]") == Vector()
    assert evalparse("[1 2 3]") == Vector(1, 2, 3)
    try:
        evalparse("a")
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

def test_to_string():
    parse = lispparser()
    assert tostring(parse("nil")) =="nil"
    assert tostring(parse("666")) =="666"
    assert tostring(parse("()")) == "()"
    assert tostring(parse("(a)")) == "(a)"
    assert tostring(parse("(a b)")) == "(a b)"
    assert tostring(parse("(a (b c))")) == "(a (b c))"
    assert tostring(parse("[]")) == "[]"
    assert tostring(parse(":a")) == ":a"

def test_scope():
    s = Scope()
    s["a"] = 666
