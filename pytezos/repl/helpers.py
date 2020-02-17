from pytezos.repl.control import instruction, do_interpret
from pytezos.repl.context import Context, StackItem
from pytezos.repl.parser import get_int
from pytezos.repl.types import Pair

helpers_prim = ['TOP', 'EXPAND', 'RUN']


@instruction('TOP', args_len=1)
def do_top(ctx: Context, prim, args, annots):
    count = min(get_int(args[0]), len(ctx.stack))
    return ctx.stack[:count]


@instruction('EXPAND', args_len=1)
def do_expand(ctx: Context, prim, args, annots):
    return args[0]


@instruction('RUN', args_len=2)
def do_run(ctx: Context, prim, args, annots):
    p_type_expr = ctx.get('parameter')
    assert p_type_expr, f'parameter type is not initialized'
    parameter = StackItem.parse(args[0], p_type_expr)

    s_type_expr = ctx.get('storage')
    assert s_type_expr, f'storage type is not initialized'
    storage = StackItem.parse(args[1], s_type_expr)

    ctx.drop_all()
    pair = Pair.new(parameter, storage)
    res = ctx.ins(pair, annots=annots)

    code = ctx.get('code')
    if code:
        res = do_interpret(ctx, code)

    return res
