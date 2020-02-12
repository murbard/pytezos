import functools
from copy import deepcopy
from pprint import pformat

from pytezos.repl.stack import Stack
from pytezos.repl.types import StackItem, assert_stack_type, assert_expr_equal, Option, Lambda, Bool, List, Or, Pair, \
    Map
from pytezos.repl.parser import get_int, MichelsonRuntimeError

instructions = {}


def assert_no_annots(prim, annots):
    assert not annots, f'unexpected annotations {annots}'


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


def parse_instruction(code_expr):
    prim = code_expr.get('prim')
    if prim not in instructions:
        raise MichelsonRuntimeError.init('unknown instruction', prim)
    args_len, handler = instructions[prim]
    args = code_expr.get('args', [])
    if len(args) != args_len:
        raise MichelsonRuntimeError.init(f'expected {args_len} arg(s), got {len(args)}', prim)
    annots = code_expr.get('annots', [])
    return prim, args, annots, handler
    

def do_interpret(stack: Stack, code_expr):
    if isinstance(code_expr, list):
        for item in code_expr:
            res = do_interpret(stack, item)
    elif isinstance(code_expr, dict):
        prim, args, annots, handler = parse_instruction(code_expr)
        try:
            res = handler(stack, prim, args, annots)
        except AssertionError as e:
            raise MichelsonRuntimeError.init(str(e), prim)
        except MichelsonRuntimeError as e:
            raise MichelsonRuntimeError.wrap(e, prim)
    else:
        assert False, f'unexpected code expression {pformat(code_expr, compact=True)}'
    return res


@instruction('PUSH', args_len=2)
def do_push(stack: Stack, prim, args, annots):
    item = StackItem.parse(val_expr=args[1], type_expr=args[0])
    return stack.ins(item, annots=annots)


@instruction('DROP', args_len=1)
def do_drop(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    count = get_int(args[0])
    _ = stack.pop_many(count=count, index=0)


@instruction('DUP')
def do_dup(stack: Stack, prim, args, annots):
    top = stack.peek()
    return stack.ins(deepcopy(top), annots=annots)


@instruction('SWAP')
def do_swap(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    second = stack.pop(index=1)
    return stack.ins(second)


@instruction('DIG', args_len=1)
def do_dig(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    index = get_int(args[0])
    res = stack.pop(index=index)
    return stack.ins(res)


@instruction('DUG', args_len=1)
def do_dug(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    index = get_int(args[0])
    res = stack.pop()
    return stack.ins(res, index=index-1)


@instruction('DIP', args_len=2)
def do_dip(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    count = get_int(args[0])
    protected = stack.pop_many(count=count)
    do_interpret(stack, args[1])
    stack.ins_many(protected)


@instruction('LAMBDA', args_len=3)
def do_lambda(stack: Stack, prim, args, annots):
    res = Lambda.new(p_type_expr=args[0], r_type_expr=args[1], code=args[2])
    return stack.ins(res, annots=annots)


@instruction('EXEC')
def do_exec(stack: Stack, prim, args, annots):
    param, lmbda = stack.pop2()
    assert_stack_type(lmbda, Lambda)
    lmbda.assert_param_type(param)
    lmbda_stack = Stack([param])
    do_interpret(lmbda_stack, lmbda.code)
    ret = lmbda_stack.pop()
    lmbda.assert_ret_type(ret)
    assert len(lmbda_stack) == 0, f'lambda stack is not empty {lmbda_stack}'
    return stack.ins(ret, annots=annots)


@instruction('APPLY')
def do_apply(stack: Stack, prim, args, annots):
    param, lmbd = stack.pop2()
    assert_stack_type(lmbd, Lambda)
    # TODO:


@instruction('FAILWITH')
def do_failwith(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    top = stack.pop()
    assert False, repr(top)


@instruction('IF', args_len=2)
def do_if(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    cond = stack.pop()
    assert_stack_type(cond, Bool)
    do_interpret(stack, args[0 if bool(cond) else 1])


@instruction('IF_CONS', args_len=2)
def do_if_cons(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    top = stack.pop()
    assert_stack_type(top, List)
    if len(top) > 0:
        stack.ins(top)
        do_interpret(stack, args[0])
    else:
        do_interpret(stack, args[1])


@instruction('IF_LEFT', args_len=2)
def do_if_left(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    top = stack.pop()  # type: Or
    assert_stack_type(top, Or)
    stack.ins(next(iter(top)))
    do_interpret(stack, args[0 if top.is_left() else 1])


@instruction('IF_NONE', args_len=2)
def do_if_left(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    top = stack.pop()
    assert_stack_type(top, Option)
    if top.is_none():
        do_interpret(stack, args[0])
    else:
        stack.ins(next(iter(top)))
        do_interpret(stack, args[1])


@instruction('LOOP', args_len=1)
def do_loop(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    while True:
        top = stack.pop()
        assert_stack_type(top, Bool)
        if bool(top):
            do_interpret(stack, args[0])
        else:
            break


@instruction('LOOP_LEFT', args_len=1)
def do_loop_left(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    while True:
        top = stack.pop()
        assert_stack_type(top, Or)
        stack.ins(next(iter(top)))
        if top.is_left():
            do_interpret(stack, args[0])
        else:
            break


@instruction('MAP', args_len=1)
def do_map(stack: Stack, prim, args, annots):
    container = stack.pop()
    assert_stack_type(container, [List, Map])

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
    return stack.ins(res, annots=annots)


@instruction('ITER', args_len=1)
def do_map(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
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
        assert False, f'unexpected type {type(container)}'


@instruction('CAST', args_len=1)
def do_cast(stack: Stack, prim, args, annots):
    assert_no_annots(prim, annots)
    top = stack.pop()
    assert_expr_equal(args[0], top.type_expr)
    top.type_expr = args[0]
    return stack.ins(top)


@instruction('RENAME')
def do_rename(stack: Stack, prim, args, annots):
    top = stack.pop()
    return stack.ins(top, annots=annots)
