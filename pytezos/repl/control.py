from pytezos.repl.instructions import primitive
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_item_type, Option, Lambda, Bool, List, Or


@primitive('LAMBDA', args_len=3)
def do_lambda(stack: Stack, prim, args):
    res = Lambda.init(p_type_expr=args[0], r_type_expr=args[1], code=args[2])
    stack.ins(res)


@primitive('EXEC')
def do_exec(stack: Stack, prim, args):
    param, lmbd = stack.pop2()
    assert_item_type(lmbd, Lambda)
    lmbd.assert_param_type(param)
    lmbd_stack = Stack([param])
    # TODO: exec code on lambda stack
    ret = lmbd_stack.pop()
    lmbd.assert_ret_type(ret)
    assert len(lmbd_stack) == 0, 'Lambda stack is not empty'
    stack.ins(ret)


@primitive('APPLY')
def do_apply(stack: Stack, prim, args):
    param, lmbd = stack.pop2()
    assert_item_type(lmbd, Lambda)
    # TODO:


@primitive('FAILWITH')
def do_failwith(stack: Stack, prim, args):
    top = stack.pop()
    raise ValueError(top)


@primitive('IF', args_len=2)
def do_if(stack: Stack, prim, args):
    cond = stack.pop()
    assert_item_type(cond, Bool)
    if cond.value:
        pass
        # TODO: exec args[0]
    else:
        pass
        # TODO: exec args[1]


@primitive('IF_CONS', args_len=2)
def do_if_cons(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, List)
    if len(top.value) > 0:
        stack.ins(top)
        # TODO: exec args[0]
    else:
        pass
        # TODO: exec args[1]


@primitive('IF_LEFT', args_len=2)
def do_if_left(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Or)
    stack.ins(top.value)
    if top.is_left():
        pass
        # TODO: exec args[0]
    else:
        pass
        # TODO: exec args[1]


@primitive('IF_NONE', args_len=2)
def do_if_left(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Option)
    if top.value is None:
        pass
        # TODO: exec args[0]
    else:
        stack.ins(top.value)
        # TODO: exec args[1]


@primitive('LOOP', args_len=1)
def do_loop(stack: Stack, prim, args):
    pass  # TODO