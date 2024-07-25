from sexpdata import Symbol
from toolz.dicttoolz import merge


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


def is_procedure(exp):
    return isinstance(exp, tuple) and exp[0] == "procedure"


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
            return ("procedure", params, body, env)
        elif is_begin(exp):
            return eval_sequence(exp[1:], env)
        else:  # Must be an application
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
    elif is_procedure(procedure):
        _, params, body, env = procedure
        fn_env = merge(env, dict(zip(params, args)))
        return eval(body, fn_env)

    raise RuntimeError(f"Apply: {repr(procedure)} to {repr(args)}")


def apply_primitive(procedure, args):
    return PRIMITIVE_PROCEDURES[procedure](*args)
