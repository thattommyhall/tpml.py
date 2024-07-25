import code
import readline
from pprint import pp
from sexpdata import loads as readsexp, Symbol

from tpml.interpreter import eval

import sys

sys.ps1 = "> "
sys.ps2 = ""


def canparse(s):
    try:
        readsexp(s)
        return True
    except Exception:
        return False


class Repl(code.InteractiveConsole):
    def __init__(self):
        self.env = {}
        super().__init__()

    def runsource(self, source, filename="<input>", symbol="single"):
        if not canparse(source):
            return True
        try:
            sexp = readsexp(source)
            if sexp == [Symbol("env")]:
                pp(self.env)
                return
            result = eval(sexp, self.env)
            pp(result)
        except Exception as e:
            print("**** ERROR ****")
            print(e)


repl = Repl()
repl.interact(banner="", exitmsg="")
