from pytezos.repl.instructions import primitive
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_item, Int, Nat, Timestamp, Mutez, Option, Pair, Bool


@primitive('ABS')
def do_abs(stack: Stack, prim, args):
    top = stack.pop()
    assert_item(top, Int)
    res = Nat.from_val(abs(top.value))
    stack.ins(res)


@primitive('ADD')
def do_add(stack: Stack, prim, args):
    left, right = stack.pop2()
    cls_mapping = {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Int, Timestamp): Timestamp,
        (Mutez, Mutez): Mutez
    }
    res_cls = cls_mapping[(type(left), type(right))]
    res = res_cls.from_val(left.value + right.value)
    stack.ins(res)


@primitive('COMPARE')
def do_compare(stack: Stack, prim, args):
    left, right = stack.pop2()
    assert type(left) == type(right), f'Cannot compare different types'
    assert left.is_comparable(), f'Not a comparable type'
    if left.value > right.value:
        res = 1
    elif left.value < right.value:
        res = -1
    else:
        res = 0
    stack.ins(Int.from_val(res))


@primitive('EDIV')
def do_ediv(stack: Stack, prim, args):
    left, right = stack.pop2()
    cls_mapping = {
        (Nat, Nat): (Nat, Nat),
        (Nat, Int): (Int, Nat),
        (Int, Nat): (Int, Nat),
        (Int, Int): (Int, Nat),
        (Mutez, Nat): (Mutez, Mutez),
        (Mutez, Mutez): (Nat, Mutez)
    }
    q_cls, r_cls = cls_mapping[(type(left), type(right))]
    if right.value == 0:
        res = Option.none(Pair.from_val((q_cls.from_val(0),
                                         r_cls.from_val(0))))
    else:
        q, r = divmod(left.value, right.value)
        if r < 0:
            r += abs(right.value)
            q += 1
        res = Option.from_val(Pair.from_val((q_cls.from_val(q),
                                             r_cls.from_val(r))))
    stack.ins(res)


@primitive('(EQ|GE|GT|LE|LT|NEQ')
def do_eq(stack: Stack, prim, args):
    top = stack.pop()
    assert_item(top, Int)
    res_mapping = {
        'EQ': lambda x: x == 0,
        'GE': lambda x: x >= 0,
        'GT': lambda x: x > 0,
        'LE': lambda x: x <= 0,
        'LT': lambda x: x < 0,
        'NEQ': lambda x: x != 0
    }
    res = Bool.from_val(res_mapping[prim](top.value))
    stack.ins(res)


@primitive('INT')
def do_int(stack: Stack, prim, args):
    top = stack.pop()
    assert_item(top, Nat)
    stack.ins(Int.from_val(top.value))


@primitive('ISNAT')
def do_is_nat(stack: Stack, prim, args):
    top = stack.pop()
    assert_item(top, Int)
    if top.value >= 0:
        res = Option.from_val(Nat.from_val(top.value))
    else:
        res = Option.none(Nat.from_val(0))
    stack.ins(res)


@primitive('(LSL|LSR)')
def do_ls(stack: Stack, prim, args):
    left, right = stack.pop2()
    assert_item(left, Nat)
    assert_item(right, Nat)
    res_mapping = {
        'LSL': lambda x: x[0] << x[1],
        'LSR': lambda x: x[0] >> x[1]
    }
    res = Nat.from_val(res_mapping[prim]((left.value, right.value)))
    stack.ins(res)


@primitive('MUL')
def do_mul(stack: Stack, prim, args):
    left, right = stack.pop2()
    cls_mapping = {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Mutez, Nat): Mutez,
        (Nat, Mutez): Mutez
    }
    res_cls = cls_mapping[(type(left), type(right))]
    res = res_cls.from_val(left.value * right.value)
    stack.ins(res)


@primitive('NEG')
def do_neg(stack: Stack, prim, args):
    top = stack.pop()
    assert type(top) in [Int, Nat], f'Unexpected type {type(top)}'
    res = Int.from_val(-top.value)
    stack.ins(res)


@primitive('SUB')
def do_sub(stack: Stack, prim, args):
    left, right = stack.pop2()
    cls_mapping = {
        (Nat, Nat): Int,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Timestamp, Timestamp): Int,
        (Mutez, Mutez): Mutez
    }
    res_cls = cls_mapping[(type(left), type(right))]
    res = res_cls.from_val(left.value - right.value)
    stack.ins(res)
