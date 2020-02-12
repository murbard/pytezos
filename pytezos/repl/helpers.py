from pytezos.repl.control import instruction
from pytezos.repl.stack import Stack, StackItem
from pytezos.repl.parser import get_int

helpers_prim = ['TOP', 'EXPAND']


@instruction('TOP', args_len=1)
def do_top(stack: Stack, prim, args, annots):
    count = min(get_int(args[0]), len(stack))
    return stack.items[:count]


@instruction('EXPAND', args_len=1)
def do_expand(stack: Stack, prim, args, annots):
    return args[0]
