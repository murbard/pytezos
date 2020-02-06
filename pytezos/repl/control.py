import functools
from copy import deepcopy

from pytezos.repl.stack import Stack
from pytezos.repl.types import StackItem, assert_type, Option, Lambda, Bool, List, Or, Pair, Map
from pytezos.repl.parser import get_int, assert_pushable

instructions = {}


def instruction(prim, args_len=0):
    def register_instruction(func):
        if isinstance(prim, list):
            for p in prim:
                instructions[p] = (args_len, func)
        else:
            instructions[prim] = (args_len, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_instruction
    

def do_interpret(stack: Stack, code_expr):
    if isinstance(code_expr, list):
        for item in code_expr:
            do_interpret(stack, item)
    elif isinstance(code_expr, dict):
        prim = code_expr.get('prim')
        assert prim in instructions, f'{prim}: unknown instruction'
        args_len, handler = instructions[prim]
        args = code_expr.get('args', [])
        assert len(args) == args_len, f'{prim}: expected {args_len} arg(s), got {len(args)}'
        return handler(stack, prim, args)
    else:
        assert False, f'unexpected code expression: {code_expr}'


@instruction('PUSH', args_len=2)
def do_push(stack: Stack, prim, args):
    assert_pushable(args[0])
    item = StackItem.parse(val_expr=args[1], type_expr=args[0])
    stack.ins(item)


@instruction('DROP', args_len=1)
def do_drop(stack: Stack, prim, args):
    count = get_int(args[0])
    _ = stack.pop_many(count=count, index=0)


@instruction('DUP')
def do_dup(stack: Stack, prim, args):
    top = stack.peek()
    stack.ins(deepcopy(top))


@instruction('SWAP')
def do_swap(stack: Stack, prim, args):
    second = stack.pop(index=1)
    stack.ins(second)


@instruction('DIG', args_len=1)
def do_dig(stack: Stack, prim, args):
    index = get_int(args[0])
    value = stack.pop(index=index)
    stack.ins(value)


@instruction('DUG', args_len=1)
def do_dug(stack: Stack, prim, args):
    index = get_int(args[0])
    value = stack.pop()
    stack.ins(value, index=index - 1)


@instruction('DIP', args_len=2)
def do_dip(stack: Stack, prim, args):
    count = get_int(args[0])
    protected = stack.pop_many(count=count, index=0)
    do_interpret(stack, args[1])
    stack.ins_many(protected)


@instruction('LAMBDA', args_len=3)
def do_lambda(stack: Stack, prim, args):
    res = Lambda.new(p_type_expr=args[0], r_type_expr=args[1], code=args[2])
    stack.ins(res)


@instruction('EXEC')
def do_exec(stack: Stack, prim, args):
    param, lmbd = stack.pop2()
    assert_type(lmbd, Lambda)
    lmbd.assert_param_type(param)
    lmbd_stack = Stack([param])
    do_interpret(lmbd_stack, lmbd.value)
    ret = lmbd_stack.pop()
    lmbd.assert_ret_type(ret)
    assert len(lmbd_stack) == 0, 'Lambda stack is not empty'
    stack.ins(ret)


@instruction('APPLY')
def do_apply(stack: Stack, prim, args):
    param, lmbd = stack.pop2()
    assert_type(lmbd, Lambda)
    # TODO:


@instruction('FAILWITH')
def do_failwith(stack: Stack, prim, args):
    top = stack.pop()
    raise ValueError(top)


@instruction('IF', args_len=2)
def do_if(stack: Stack, prim, args):
    cond = stack.pop()
    assert_type(cond, Bool)
    do_interpret(stack, args[0 if cond.value else 1])


@instruction('IF_CONS', args_len=2)
def do_if_cons(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, List)
    if len(top.value) > 0:
        stack.ins(top)
        do_interpret(stack, args[0])
    else:
        do_interpret(stack, args[1])


@instruction('IF_LEFT', args_len=2)
def do_if_left(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Or)
    stack.ins(top.value)
    do_interpret(stack, args[0 if top.is_left() else 1])


@instruction('IF_NONE', args_len=2)
def do_if_left(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Option)
    if top.value is None:
        do_interpret(stack, args[0])
    else:
        stack.ins(top.value)
        do_interpret(stack, args[1])


@instruction('LOOP', args_len=1)
def do_loop(stack: Stack, prim, args):
    pass  # TODO


@instruction('MAP', args_len=1)
def do_map(stack: Stack, prim, args):
    container = stack.pop()
    assert_type(container, [List, Map])

    if type(container) == List:
        items = list()
        for item in container:
            stack.ins(item)
            do_interpret(stack, args[0])
            ret = stack.pop()
            container.assert_val_type(ret)
            items.append(ret)
    elif type(container) == Map:
        items = list()
        for key, val in container:
            stack.ins(Pair.new(key, val))
            do_interpret(stack, args[0])
            ret = stack.pop()
            container.assert_val_type(ret)
            items.append((key, ret))
    else:
        assert False

    res = type(container).new(items)
    stack.ins(res)


@instruction('ITER', args_len=1)
def do_map(stack: Stack, prim, args):
    container = stack.pop()
    if type(container) == List:
        for item in container:
            stack.ins(item)
            do_interpret(stack, args[0])
    elif type(container) == Map:
        for key, val in container:
            stack.ins(Pair.new(key, val))
            do_interpret(stack, args[0])
    else:
        assert False, f'Unexpected type: {type(container)}'
