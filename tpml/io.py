from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.absolute()

from sexpdata import Symbol, Parser


class PerverseParser(Parser):
    def atom(self, token):
        # We don't understand anything
        return Symbol(token)


def readsexp(string, **kwds):
    assert type(string) == str
    obj = PerverseParser(string, **kwds).parse()
    if len(obj) != 1:
        raise (RuntimeError("Invalid S-Expression"))
    return obj[0]


def load_scm(filename):
    with (BASE_PATH / filename).open() as f:
        result = readsexp(f.read())
    return result
