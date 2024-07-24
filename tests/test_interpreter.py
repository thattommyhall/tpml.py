from sexpdata import loads, Symbol
from pytest import raises

# pylint: disable-next=redefined-builtin
from tpml.interpreter import eval, concat, SchemeError, is_begin, str_equal
from tpml.io import load_scm


def assert_result(s, value, env=None):
    if env is None:
        assert_result(s, value, {})
    assert eval(loads(s), env) == value


def test_self_evaluating():
    assert_result('"Hello"', "Hello")


def test_var_lookup():
    assert eval(Symbol("a"), {Symbol("a"): 3}) == 3


def test_define():
    env = {}
    exp = loads('(define a "hello")')
    eval(exp, env)
    assert env == {Symbol("a"): "hello"}


def test_concat():
    assert concat("Hello ", "World") == "Hello World"


def test_lambda():
    assert eval(loads("(lambda (x y) (+ x y))"), {}) == (
        "procedure",
        [Symbol("x"), Symbol("y")],
        [Symbol("+"), Symbol("x"), Symbol("y")],
        {},
    )


def test_apply_primitive():
    assert eval(loads('(concat "Hello " "World")'), {}) == "Hello World"


def test_raises():
    with raises(SchemeError):
        eval(loads('(raise "TestError")'), {})


def test_apply():
    test_sexp = """((lambda (x y) (concat x y))
                    "Hello " "World")"""
    assert eval(loads(test_sexp), {}) == "Hello World"


def test_begin():
    exp = load_scm("tests/scm/begin.scm")
    assert is_begin(exp)
    assert eval(exp, {}) == "begin somewhere"

def test_str_equal():
    assert str_equal("one", "one", "one")
    assert not str_equal("one", "two", "one")

    assert eval(loads('(str= "one" "one" "one")'), {}) == Symbol("t")
