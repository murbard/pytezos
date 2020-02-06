from hashlib import sha256, sha512

from pytezos.crypto import blake2b_32, Key
from pytezos.repl.control import instruction
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_type, Int, Nat, Timestamp, Mutez, Option, Pair, Bool, Bytes, Key, Signature, \
    KeyHash


def assert_supported_types(a, b, mapping):
    assert (type(a), type(b)) in mapping, \
        f'unsupported argument types {type(a).__name__} and {type(b).__name__}'


def assert_equal_types(a, b):
    assert type(a) == type(b), f'different types {type(a).__name__} and {type(b).__name__}'


def assert_comparable(a, prim):
    assert a.is_comparable(), f'{type(a).__name__} is not a comparable type'


@instruction('ABS')
def do_abs(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Int, prim)
    res = Nat(abs(top.value))
    stack.ins(res)


@instruction('ADD')
def do_add(stack: Stack, prim, args):
    a, b = stack.pop2()
    mapping = {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Int, Timestamp): Timestamp,
        (Mutez, Mutez): Mutez
    }
    assert_supported_types(a, b, mapping)
    res_cls = mapping[(type(a), type(b))]
    res = res_cls(a.value + b.value)
    stack.ins(res)


@instruction('COMPARE')
def do_compare(stack: Stack, prim, args):
    a, b = stack.pop2()
    assert_equal_types(a, b)
    assert_comparable(a, prim)
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
    mapping = {
        (Nat, Nat): (Nat, Nat),
        (Nat, Int): (Int, Nat),
        (Int, Nat): (Int, Nat),
        (Int, Int): (Int, Nat),
        (Mutez, Nat): (Mutez, Mutez),
        (Mutez, Mutez): (Nat, Mutez)
    }
    assert_supported_types(a, b, mapping)
    q_cls, r_cls = mapping[(type(a), type(b))]
    if b.value == 0:
        res = Option.none(Pair(q_cls(), r_cls()).type_expr)
    else:
        q, r = divmod(a.value, b.value)
        if r < 0:
            r += abs(b.value)
            q += 1
        res = Option.some(Pair(q_cls(q), r_cls(r)))
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
    mapping = {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Mutez, Nat): Mutez,
        (Nat, Mutez): Mutez
    }
    assert_supported_types(a, b, mapping)
    res_cls = mapping[(type(a), type(b))]
    res = res_cls(a.value * b.value)
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
    mapping = {
        (Nat, Nat): Int,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Timestamp, Int): Timestamp,
        (Timestamp, Timestamp): Int,
        (Mutez, Mutez): Mutez
    }
    assert_supported_types(a, b, mapping)
    res_cls = mapping[(type(a), type(b))]
    res = res_cls(a.value - b.value)
    stack.ins(res)


@instruction(['AND', 'OR', 'XOR'])
def do_and(stack: Stack, prim, args):
    a, b = stack.pop2()
    assert_type(a, [Bool, Nat])
    assert_equal_types(a, b)
    res_cls = type(a)
    handlers = {
        'AND': lambda x: x[0] & x[1],
        'OR': lambda x: x[0] | x[1],
        'XOR': lambda x: x[0] ^ x[1]
    }
    res = res_cls(handlers[prim](a.value, b.value))
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
