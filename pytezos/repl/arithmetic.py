from pytezos.repl.instructions import primitive
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_item_type, Int, Nat, Timestamp, Mutez, Option, Pair, Bool


@primitive('ABS')
def do_abs(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Int)
    res = Nat(abs(top.value))
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
    res = res_cls(left.value + right.value)
    stack.ins(res)


@primitive('COMPARE')
def do_compare(stack: Stack, prim, args):
    left, right = stack.pop2()
    assert type(left) == type(right), f'Cannot compare different types'
    assert left.is_comparable(), f'Not a comparable type: {type(left)}'
    if left.value > right.value:
        res = Int(1)
    elif left.value < right.value:
        res = Int(-1)
    else:
        res = Int(0)
    stack.ins(res)


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
        res = Option.none(Pair(q_cls(), r_cls()).type_expr)
    else:
        q, r = divmod(left.value, right.value)
        if r < 0:
            r += abs(right.value)
            q += 1
        res = Option.some(Pair(q_cls(q), r_cls(r)))
    stack.ins(res)


@primitive('(EQ|GE|GT|LE|LT|NEQ')
def do_eq(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Int)
    res_mapping = {
        'EQ': lambda x: x == 0,
        'GE': lambda x: x >= 0,
        'GT': lambda x: x > 0,
        'LE': lambda x: x <= 0,
        'LT': lambda x: x < 0,
        'NEQ': lambda x: x != 0
    }
    res = Bool(res_mapping[prim](top.value))
    stack.ins(res)


@primitive('INT')
def do_int(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Nat)
    res = Int(top.value)
    stack.ins(res)


@primitive('ISNAT')
def do_is_nat(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Int)
    if top.value >= 0:
        res = Option.some(Nat(top.value))
    else:
        res = Option.none(Nat().type_expr)
    stack.ins(res)


@primitive('(LSL|LSR)')
def do_lsl(stack: Stack, prim, args):
    left, right = stack.pop2()
    assert_item_type(left, Nat)
    assert_item_type(right, Nat)
    res_mapping = {
        'LSL': lambda x: x[0] << x[1],
        'LSR': lambda x: x[0] >> x[1]
    }
    res = Nat(res_mapping[prim]((left.value, right.value)))
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
    res = res_cls(left.value * right.value)
    stack.ins(res)


@primitive('NEG')
def do_neg(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, [Int, Nat])
    res = Int(-top.value)
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
    res = res_cls(left.value - right.value)
    stack.ins(res)


@primitive('(AND|OR|XOR')
def do_and(stack: Stack, prim, args):
    left, right = stack.pop2()
    assert_item_type(left, [Bool, Nat])
    assert type(left) == type(right), f'Cannot operate on different types'
    res_cls = type(left)
    res_mapping = {
        'AND': lambda x: x[0] & x[1],
        'OR': lambda x: x[0] | x[1],
        'XOR': lambda x: x[0] ^ x[1]
    }
    res = res_cls(res_mapping[prim](left.value, right.value))
    stack.ins(res)


@primitive('NOT')
def do_not(stack: Stack, prim, args):
    top = stack.pop()
    if type(top) in [Nat, Int]:
        res = Int(~top.value)
    elif type(top) == Bool:
        res = Bool(not top.value)
    else:
        assert False, f'Unexpected type {type(top)}'
    stack.ins(res)
