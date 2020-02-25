import functools
from copy import deepcopy
from pprint import pformat

from pytezos.repl.context import Context
from pytezos.repl.types import StackItem, assert_stack_type, assert_expr_equal, Option, Lambda, Bool, List, Or, Pair, \
    Map, Int
from pytezos.repl.parser import get_int, MichelsonRuntimeError, assert_pushable, parse_prim_expr

instructions = {}


def assert_no_annots(prim, annots):
    assert not annots, f'unexpected annotations {annots}'


def instruction(prim, args_len=0):
    def register_instruction(func):
        if isinstance(prim, list):
            for p in prim:
                instructions[(p, args_len)] = func
        else:
            instructions[(prim, args_len)] = func

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_instruction


def parse_instruction(code_expr):
    prim, args = parse_prim_expr(code_expr)
    key = (prim, len(args))
    if key not in instructions:
        raise MichelsonRuntimeError.init(f'unknown instruction: {key}', prim)
    handler = instructions[key]
    annots = code_expr.get('annots', [])
    return prim, args, annots, handler
    

def do_interpret(ctx: Context, code_expr):
    res = None
    if isinstance(code_expr, list):
        for item in code_expr:
            res = do_interpret(ctx, item)
    elif isinstance(code_expr, dict):
        prim, args, annots, handler = parse_instruction(code_expr)
        try:
            ctx.begin(prim)
            res = handler(ctx, prim, args, annots)
        except AssertionError as e:
            raise MichelsonRuntimeError.init(str(e), prim)
        except MichelsonRuntimeError as e:
            raise MichelsonRuntimeError.wrap(e, prim)
        finally:
            ctx.end()
    else:
        assert False, f'unexpected code expression {pformat(code_expr, compact=True)}'
    return res


@instruction('PUSH', args_len=2)
def do_push(ctx: Context, prim, args, annots):
    item = StackItem.parse(val_expr=args[1], type_expr=args[0])
    assert_pushable(item.type_expr)
    ctx.push(item, annots=annots)


@instruction('DROP', args_len=1)
def do_drop(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    count = get_int(args[0])
    _ = ctx.pop_many(count=count)


@instruction('DUP')
def do_dup(ctx: Context, prim, args, annots):
    top = ctx.peek()
    ctx.push(deepcopy(top), annots=annots)


@instruction('SWAP')
def do_swap(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    a, b = ctx.pop2()
    ctx.push_many([b, a])


@instruction('DIG', args_len=1)
def do_dig(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    index = get_int(args[0])
    ctx.protect(index)
    res = ctx.pop()
    ctx.push(res)
    ctx.restore(index)


@instruction('DUG', args_len=1)
def do_dug(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    index = get_int(args[0])
    res = ctx.pop()
    ctx.protect(index - 1)
    ctx.push(res)
    ctx.restore(index - 1)


@instruction('DIP', args_len=2)
def do_dip(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    count = get_int(args[0])
    ctx.protect(count)
    do_interpret(ctx, args[1])
    ctx.restore(count)


@instruction('DIP', args_len=1)
def do_dip_1(ctx: Context, prim, args, annots):
    return do_dip(ctx, prim, [{'int': '1'}, args[0]], annots)


@instruction('LAMBDA', args_len=3)
def do_lambda(ctx: Context, prim, args, annots):
    res = Lambda.new(p_type_expr=args[0], r_type_expr=args[1], code=args[2])
    ctx.push(res, annots=annots)


@instruction('EXEC')
def do_exec(ctx: Context, prim, args, annots):
    param, lmbda = ctx.pop2()
    assert_stack_type(lmbda, Lambda)
    lmbda.assert_param_type(param)
    lmbda_ctx = Context([param])
    do_interpret(lmbda_ctx, lmbda.code)
    ret = lmbda_ctx.pop()
    lmbda.assert_ret_type(ret)
    assert len(lmbda_ctx) == 0, f'lambda ctx is not empty {lmbda_ctx}'
    ctx.push(ret, annots=annots)


@instruction('APPLY')
def do_apply(ctx: Context, prim, args, annots):
    param, lmbda = ctx.pop2()
    assert_stack_type(lmbda, Lambda)
    res = lmbda.partial_apply(param)
    ctx.push(res)


@instruction('FAILWITH')
def do_failwith(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    top = ctx.pop()
    assert False, repr(top)


@instruction('IF', args_len=2)
def do_if(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    cond = ctx.pop()
    assert_stack_type(cond, Bool)
    do_interpret(ctx, args[0 if bool(cond) else 1])


@instruction('IF_CONS', args_len=2)
def do_if_cons(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    top = ctx.pop()
    assert_stack_type(top, List)
    if len(top) > 0:
        ctx.push(top)
        do_interpret(ctx, args[0])
    else:
        do_interpret(ctx, args[1])


@instruction('IF_LEFT', args_len=2)
def do_if_left(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    top = ctx.pop()  # type: Or
    assert_stack_type(top, Or)
    ctx.push(next(iter(top)))
    do_interpret(ctx, args[0 if top.is_left() else 1])


@instruction('IF_NONE', args_len=2)
def do_if_left(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    top = ctx.pop()
    assert_stack_type(top, Option)
    if top.is_none():
        do_interpret(ctx, args[0])
    else:
        ctx.push(next(iter(top)))
        do_interpret(ctx, args[1])


@instruction('LOOP', args_len=1)
def do_loop(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    while True:
        top = ctx.pop()
        assert_stack_type(top, Bool)
        if bool(top):
            do_interpret(ctx, args[0])
        else:
            break


@instruction('LOOP_LEFT', args_len=1)
def do_loop_left(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    while True:
        top = ctx.pop()
        assert_stack_type(top, Or)
        ctx.push(next(iter(top)))
        if top.is_left():
            do_interpret(ctx, args[0])
        else:
            break


@instruction('MAP', args_len=1)
def do_map(ctx: Context, prim, args, annots):
    container = ctx.pop()
    assert_stack_type(container, [List, Map])

    if type(container) == List:
        items = list()
        for item in container:
            ctx.push(item)
            do_interpret(ctx, args[0])
            ret = ctx.pop()
            container.assert_val_type(ret)
            items.append(ret)
    elif type(container) == Map:
        items = list()
        for key, val in container:
            ctx.push(Pair.new(key, val))
            do_interpret(ctx, args[0])
            ret = ctx.pop()
            container.assert_val_type(ret)
            items.append((key, ret))
    else:
        assert False

    res = type(container).new(items)
    ctx.push(res, annots=annots)


@instruction('ITER', args_len=1)
def do_map(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    container = ctx.pop()
    if type(container) == List:
        for item in container:
            ctx.push(item)
            do_interpret(ctx, args[0])
    elif type(container) == Map:
        for key, val in container:
            ctx.push(Pair.new(key, val))
            do_interpret(ctx, args[0])
    else:
        assert False, f'unexpected type {type(container)}'


@instruction('CAST', args_len=1)
def do_cast(ctx: Context, prim, args, annots):
    assert_no_annots(prim, annots)
    top = ctx.pop()
    assert_expr_equal(args[0], top.type_expr)
    top.type_expr = args[0]
    ctx.push(top)


@instruction('RENAME')
def do_rename(ctx: Context, prim, args, annots):
    top = ctx.pop()
    ctx.push(top, annots=annots)
