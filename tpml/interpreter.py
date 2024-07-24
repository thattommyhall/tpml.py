from sexpdata import Symbol
from toolz.dicttoolz import merge


def is_self_evaluating(exp):
    # pylint: disable-next=unidiomatic-typecheck
    return type(exp) == str or (isinstance(exp, Symbol) and exp in PRIMITIVE_PROCEDURES)
    # (Symbol is an instance of str too)


def is_variable(exp):
    return isinstance(exp, Symbol) and not exp in PRIMITIVE_PROCEDURES


def is_def(exp):
    return len(exp) == 3 and exp[0] == Symbol("define")


def unpack_def_exp(exp):
    return exp[1], exp[2]


def is_lambda(exp):
    return len(exp) == 3 and exp[0] == Symbol("lambda")


def unpack_lambda_exp(exp):
    return exp[1], exp[2]


def is_application(exp):
    return isinstance(exp, list)


def concat(*args):
    return "".join(args)


class SchemeError(Exception):
    pass


def prim_raise(message):
    raise SchemeError(message)


PRIMITIVE_PROCEDURES = {Symbol("concat"): concat, Symbol("raise"): prim_raise}


# pylint: disable-next=redefined-builtin
def eval(exp, env):
    if is_self_evaluating(exp):
        return exp
    elif is_variable(exp):
        return env[exp]
    elif is_def(exp):
        name, value = unpack_def_exp(exp)
        env[name] = eval(value, env)
    elif is_lambda(exp):
        params, body = unpack_lambda_exp(exp)
        return ("procedure", params, body, env)
    elif is_application(exp):
        operator = eval(exp[0], env)
        operands = [eval(operand, env) for operand in exp[1:]]
        return apply(operator, operands)
    else:
        raise RuntimeError(f"Eval {repr(exp)} in {repr(env)}")


def eval_sequence(exps, env):
    result = None
    for exp in exps:
        print(exp)
        result = eval(exp, env)
        print(result)
    return result


def is_procedure(exp):
    return isinstance(exp, tuple) and exp[0] == "procedure"


def is_primitive(exp):
    return isinstance(exp, Symbol) and exp in PRIMITIVE_PROCEDURES


def apply_primitive(procedure, args):
    return PRIMITIVE_PROCEDURES[procedure](*args)


def apply(procedure, args):
    if is_primitive(procedure):
        return apply_primitive(procedure, args)
    elif is_procedure(procedure):
        _, params, body, env = procedure
        fn_env = merge(env, dict(zip(params, args)))
        return eval(body, fn_env)

    raise RuntimeError(f"Apply: {repr(procedure)} to {repr(args)}")
