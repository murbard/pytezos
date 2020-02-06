from hashlib import sha256, sha512

from pytezos.crypto import blake2b_32, Key
from pytezos.repl.control import instruction
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_type, Int, Nat, Timestamp, Mutez, Option, Pair, Bool, Bytes, Key, Signature, \
    KeyHash
from pytezos.repl.parser import assert_comparable, assert_expr_equal


def dispatch_type_map(a, b, mapping):
    assert (type(a), type(b)) in mapping, \
        f'unsupported argument types {type(a).__name__} and {type(b).__name__}'
    return mapping[(type(a), type(b))]


def assert_equal_types(a, b):
    assert type(a) == type(b), f'different types {type(a).__name__} and {type(b).__name__}'


@instruction('ABS')
def do_abs(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Int)
    res = Nat(abs(top.value))
    stack.ins(res)


@instruction('ADD')
def do_add(stack: Stack, prim, args):
    a, b = stack.pop2()
    res_type = dispatch_type_map(a, b, {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Int, Timestamp): Timestamp,
        (Mutez, Mutez): Mutez
    })
    res = res_type(a.value + b.value)
    stack.ins(res)


@instruction('COMPARE')
def do_compare(stack: Stack, prim, args):
    a, b = stack.pop2()
    assert_expr_equal(a.type_expr, b.type_expr)
    assert_comparable(a.type_expr)
    if a.value > b.value:
        res = Int(1)
    elif a.value < b.value:
        res = Int(-1)
    else:
        res = Int(0)
    stack.ins(res)


@instruction('EDIV')
def do_ediv(stack: Stack, prim, args):
    a, b = stack.pop2()
    q_type, r_type = dispatch_type_map(a, b, {
        (Nat, Nat): (Nat, Nat),
        (Nat, Int): (Int, Nat),
        (Int, Nat): (Int, Nat),
        (Int, Int): (Int, Nat),
        (Mutez, Nat): (Mutez, Mutez),
        (Mutez, Mutez): (Nat, Mutez)
    })
    if b.value == 0:
        res = Option.none(Pair.new(q_type(), r_type()).type_expr)
    else:
        q, r = divmod(a.value, b.value)
        if r < 0:
            r += abs(b.value)
            q += 1
        res = Option.some(Pair.new(q_type(q), r_type(r)))
    stack.ins(res)


@instruction(['EQ', 'GE', 'GT', 'LE', 'LT', 'NEQ'])
def do_eq(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Int)
    handlers = {
        'EQ': lambda x: x == 0,
        'GE': lambda x: x >= 0,
        'GT': lambda x: x > 0,
        'LE': lambda x: x <= 0,
        'LT': lambda x: x < 0,
        'NEQ': lambda x: x != 0
    }
    res = Bool(handlers[prim](top.value))
    stack.ins(res)


@instruction('INT')
def do_int(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Nat)
    res = Int(top.value)
    stack.ins(res)


@instruction('ISNAT')
def do_is_nat(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Int)
    if top.value >= 0:
        res = Option.some(Nat(top.value))
    else:
        res = Option.none(Nat().type_expr)
    stack.ins(res)


@instruction(['LSL', 'LSR'])
def do_lsl(stack: Stack, prim, args):
    a, b = stack.pop2()
    assert_type(a, Nat)
    assert_type(b, Nat)
    handlers = {
        'LSL': lambda x: x[0] << x[1],
        'LSR': lambda x: x[0] >> x[1]
    }
    res = Nat(handlers[prim]((a.value, b.value)))
    stack.ins(res)


@instruction('MUL')
def do_mul(stack: Stack, prim, args):
    a, b = stack.pop2()
    res_type = dispatch_type_map(a, b, {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Mutez, Nat): Mutez,
        (Nat, Mutez): Mutez
    })
    res = res_type(a.value * b.value)
    stack.ins(res)


@instruction('NEG')
def do_neg(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, [Int, Nat])
    res = Int(-top.value)
    stack.ins(res)


@instruction('SUB')
def do_sub(stack: Stack, prim, args):
    a, b = stack.pop2()
    res_type = dispatch_type_map(a, b, {
        (Nat, Nat): Int,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Timestamp, Timestamp): Int,
        (Mutez, Mutez): Mutez
    })
    res = res_type(a.value - b.value)
    stack.ins(res)


@instruction(['AND', 'OR', 'XOR'])
def do_and(stack: Stack, prim, args):
    a, b = stack.pop2()
    assert_type(a, [Bool, Nat])
    assert_equal_types(a, b)
    handlers = {
        'AND': lambda x: x[0] & x[1],
        'OR': lambda x: x[0] | x[1],
        'XOR': lambda x: x[0] ^ x[1]
    }
    res_type = type(a)
    res = res_type(handlers[prim]((a.value, b.value)))
    stack.ins(res)


@instruction('NOT')
def do_not(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, [Nat, Int, Bool])
    if type(top) in [Nat, Int]:
        res = Int(~top.value)
    elif type(top) == Bool:
        res = Bool(not top.value)
    else:
        assert False
    stack.ins(res)


@instruction('BLAKE2B')
def do_blake2b(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Bytes)
    res = Bytes(blake2b_32(top.value).digest())
    stack.ins(res)


@instruction('CHECK_SIGNATURE')
def do_check_sig(stack: Stack, prim, args):
    pk, sig, msg = stack.pop3()
    assert_type(pk, Key)
    assert_type(sig, Signature)
    assert_type(msg, Bytes)
    key = Key.from_encoded_key(pk.value)
    try:
        key.verify(signature=sig.value, message=msg.value)
    except:
        res = Bool(False)
    else:
        res = Bool(True)
    stack.ins(res)


@instruction('HASH_KEY')
def do_hash_key(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Key)
    key = Key.from_encoded_key(top.value)
    res = KeyHash(key.public_key_hash())
    stack.ins(res)


@instruction(['SHA256', 'SHA512'])
def do_sha(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Bytes)
    handlers = {
        'SHA256': lambda x: sha256(x).digest(),
        'SHA512': lambda x: sha512(x).digest(),
    }
    res = Bytes(handlers[prim](top.value))
    stack.ins(res)
