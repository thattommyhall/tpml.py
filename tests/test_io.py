from sexpdata import Symbol
from tpml.io import load_scm


def test_load_scm():
    assert load_scm("tests/scm/00.scm") == [
        Symbol("+"),
        Symbol("1"),
        Symbol("2"),
        Symbol("3"),
    ]
