from sexpdata import Symbol
from toolz.dicttoolz import merge
from dataclasses import dataclass
import sys

sys.setrecursionlimit(2**20)


def str_equal(*args):
    first = args[0]
    return all([s == first for s in args])


def prim_concat(*args):
    return "".join(args)


def prim_str_equal(*args):
    if str_equal(*args):
        return Symbol("#t")
    else:
        return Symbol("#f")


@dataclass
class SchemeProcedure:
    params: list
    body: list
    env: dict

    def __repr__(self) -> str:
        return {"params": self.params, "body": self.body}.__repr__()


class SchemeError(Exception):
    pass


def prim_raise(message):
    raise SchemeError(message)


PRIMITIVE_PROCEDURES = {
    Symbol("concat"): prim_concat,
    Symbol("raise"): prim_raise,
    Symbol("str="): prim_str_equal,
}

SELF_EVALUATING = list(PRIMITIVE_PROCEDURES.keys()) + [Symbol("#t"), Symbol("#f")]


def is_primitive(exp):
    return isinstance(exp, Symbol) and exp in PRIMITIVE_PROCEDURES


def is_self_evaluating(exp):
    # pylint: disable-next=unidiomatic-typecheck
    return type(exp) == str or (isinstance(exp, Symbol) and exp in SELF_EVALUATING)
    # (Symbol is an instance of str too)


def is_variable(exp):
    return isinstance(exp, Symbol) and not exp in SELF_EVALUATING


def is_begin(exp):
    return exp[0] == Symbol("begin")


def is_def(exp):
    return len(exp) == 3 and exp[0] == Symbol("define")


def is_lambda(exp):
    return len(exp) == 3 and exp[0] == Symbol("lambda")


def is_if(exp):
    return len(exp) in [3, 4] and exp[0] == Symbol("if")


# pylint: disable-next=redefined-builtin
def eval(exp, env):
    if is_self_evaluating(exp):
        return exp
    if is_variable(exp):
        return env[exp]
    if isinstance(exp, list):
        if is_def(exp):
            name, value = exp[1], exp[2]
            env[name] = eval(value, env)
            return
        elif is_if(exp):
            test, consequent = exp[1], exp[2]
            if eval(test, env) == Symbol("#t"):
                return eval(consequent, env)
            if len(exp) == 4:
                alternative = exp[3]
                return eval(alternative, env)
            return Symbol("Nothing")
        elif is_lambda(exp):
            params, body = exp[1], exp[2]
            return SchemeProcedure(params, body, env)
        elif is_begin(exp):
            return eval_sequence(exp[1:], env)
        else:  # Must be an application at this point
            operator = eval(exp[0], env)
            operands = [eval(operand, env) for operand in exp[1:]]
            return apply(operator, operands)
    raise RuntimeError(f"Cannot eval: {repr(exp)}")


def eval_sequence(exps, env):
    result = None
    for exp in exps:
        result = eval(exp, env)
    return result


def apply(procedure, args):
    if is_primitive(procedure):
        return apply_primitive(procedure, args)
    elif isinstance(procedure, SchemeProcedure):
        fn_env = merge(procedure.env, dict(zip(procedure.params, args)))
        return eval(procedure.body, fn_env)

    raise RuntimeError(f"Apply: {repr(procedure)} to {repr(args)}")


def apply_primitive(procedure, args):
    return PRIMITIVE_PROCEDURES[procedure](*args)
