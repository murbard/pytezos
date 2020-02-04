import functools
from copy import deepcopy

from pytezos.repl.stack import Stack
from pytezos.repl.types import StackItem, assert_type

instructions = {}


def primitive(prim, args_len=0):
    def register_primitive(func):
        instructions[prim] = (args_len, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_primitive


def parse_int(val_node):
    assert_type(val_node, core_type='int')
    return int(val_node['int'])


def do_interpret(stack: Stack, code):
    pass


@primitive('PUSH', args_len=2)
def do_push(stack: Stack, args):
    stack.ins(StackItem.parse(args[0], args[1]))


@primitive('DROP', args_len=1)
def do_drop(stack: Stack, args):
    count = parse_int(args[0])
    _ = stack.pop_many(count=count, index=0)


@primitive('DUP')
def do_dup(stack: Stack, args):
    top = stack.peek()
    stack.ins(deepcopy(top))


@primitive('SWAP')
def do_swap(stack: Stack, args):
    second = stack.pop(index=1)
    stack.ins(second)


@primitive('DIG', args_len=1)
def do_dig(stack: Stack, args):
    index = parse_int(args[0])
    value = stack.pop(index=index)
    stack.ins(value)


@primitive('DUG', args_len=1)
def do_dug(stack: Stack, args):
    index = parse_int(args[0])
    value = stack.pop()
    stack.ins(value, index=index - 1)


@primitive('DIP', args_len=2)
def do_dip(stack: Stack, args):
    count = parse_int(args[0])
    protected = stack.pop_many(count=count, index=0)
    do_interpret(stack=stack, code=args[1])
    stack.ins_many(protected)


@primitive('ABS')
def do_abs(stack: Stack, args):
    top = stack.pop()
    stack.ins(abs(top))


@primitive('ADD')
def do_add(stack: Stack, args):
    left, right = stack.pop2()
    stack.ins(left + right)


@primitive('COMPARE')
def do_compare(stack: Stack, args):
    left, right = stack.pop2()
    stack.ins(left.__cmp__(right))
