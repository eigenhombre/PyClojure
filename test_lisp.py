from lisp_lex import lisplexer  # Need tokens for parser
from lisp_yacc import lispparser
from lisp_core import (Atom, List, Scope, evaluate, tostring,
                       UnknownVariable)

def test_lexer():
    lexer = lisplexer()
    lexer.input("""(a 
                      (nested) list (of 534 atoms 
                          (and lists)))  ;; with comments
                """)
    assert 16 == len([tok for tok in lexer])
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
    assert Atom() == Atom()
    assert List() == List()
    assert List(1) == List(1)
    assert List(2) != List(1)
    assert List(1, 2) != List(2, 1)
    assert List(1, 2) == List(1, 2)
    assert List(Atom()) == List(Atom())
    assert List(Atom('a')) == List(Atom('a'))
    assert List(Atom('b')) != List(Atom('a'))


def test_eval():
    parse = lispparser()
    scopechain = [Scope()]
    assert evaluate(parse("666"), scopechain) == 666
    assert evaluate(parse("nil"), scopechain) == None
    assert evaluate(parse("()"), scopechain) == List()
    try:
        evaluate(parse("a"), scopechain)
        assert False, "UnknownVariable exception not raised!"
    except UnknownVariable:
        pass
    scopechain[-1]["a"] = 777
    assert evaluate(parse("a"), scopechain) == 777
    evaluate(parse("(def a 666)"), scopechain)
    assert evaluate(parse("a"), scopechain) == 666


def test_to_string():
    parse = lispparser()
    assert tostring(parse("nil")) =="nil"
    assert tostring(parse("666")) =="666"
    assert tostring(parse("()")) == "()"
    assert tostring(parse("(a)")) == "(a)"
    assert tostring(parse("(a b)")) == "(a b)"
    assert tostring(parse("(a (b c))")) == "(a (b c))"

def test_scope():
    s = Scope()
    s["a"] = 666