from hashlib import sha256, sha512

from pytezos.crypto import blake2b_32, Key
from pytezos.repl.control import instruction
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_stack_type, Int, Nat, Timestamp, Mutez, Option, Pair, Bool, Bytes, Key, \
    Signature, KeyHash, dispatch_type_map


@instruction('ABS')
def do_abs(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Int)
    res = Nat(abs(int(top)))
    return stack.ins(res, annots=annots)


@instruction('ADD')
def do_add(stack: Stack, prim, args, annots):
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
    res = res_type(int(a) + int(b))
    return stack.ins(res, annots=annots)


@instruction('COMPARE')
def do_compare(stack: Stack, prim, args, annots):
    a, b = stack.pop2()
    res = Int(a.__cmp__(b))
    return stack.ins(res, annots=annots)


@instruction('EDIV')
def do_ediv(stack: Stack, prim, args, annots):
    a, b = stack.pop2()
    q_type, r_type = dispatch_type_map(a, b, {
        (Nat, Nat): (Nat, Nat),
        (Nat, Int): (Int, Nat),
        (Int, Nat): (Int, Nat),
        (Int, Int): (Int, Nat),
        (Mutez, Nat): (Mutez, Mutez),
        (Mutez, Mutez): (Nat, Mutez)
    })
    if int(b) == 0:
        res = Option.none(Pair.new(q_type(), r_type()).type_expr)
    else:
        q, r = divmod(int(a), int(b))
        if r < 0:
            r += abs(int(b))
            q += 1
        res = Option.some(Pair.new(q_type(q), r_type(r)))
    return stack.ins(res, annots=annots)


@instruction(['EQ', 'GE', 'GT', 'LE', 'LT', 'NEQ'])
def do_eq(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Int)
    handlers = {
        'EQ': lambda x: x == 0,
        'GE': lambda x: x >= 0,
        'GT': lambda x: x > 0,
        'LE': lambda x: x <= 0,
        'LT': lambda x: x < 0,
        'NEQ': lambda x: x != 0
    }
    res = Bool(handlers[prim](int(top)))
    return stack.ins(res, annots=annots)


@instruction('INT')
def do_int(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Nat)
    res = Int(int(top))
    return stack.ins(res, annots=annots)


@instruction('ISNAT')
def do_is_nat(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Int)
    if int(top) >= 0:
        res = Option.some(Nat(int(top)))
    else:
        res = Option.none(Nat().type_expr)
    return stack.ins(res, annots=annots)


@instruction(['LSL', 'LSR'])
def do_lsl(stack: Stack, prim, args, annots):
    a, b = stack.pop2()
    assert_stack_type(a, Nat)
    assert_stack_type(b, Nat)
    handlers = {
        'LSL': lambda x: x[0] << x[1],
        'LSR': lambda x: x[0] >> x[1]
    }
    res = Nat(handlers[prim]((int(a), int(b))))
    return stack.ins(res, annots=annots)


@instruction('MUL')
def do_mul(stack: Stack, prim, args, annots):
    a, b = stack.pop2()
    res_type = dispatch_type_map(a, b, {
        (Nat, Nat): Nat,
        (Nat, Int): Int,
        (Int, Nat): Int,
        (Int, Int): Int,
        (Mutez, Nat): Mutez,
        (Nat, Mutez): Mutez
    })
    res = res_type(int(a) * int(b))
    return stack.ins(res, annots=annots)


@instruction('NEG')
def do_neg(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, [Int, Nat])
    res = Int(-int(top))
    return stack.ins(res, annots=annots)


@instruction('SUB')
def do_sub(stack: Stack, prim, args, annots):
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
    res = res_type(int(a) - int(b))
    return stack.ins(res, annots=annots)


@instruction(['AND', 'OR', 'XOR'])
def do_and(stack: Stack, prim, args, annots):
    a, b = stack.pop2()
    val_type = dispatch_type_map(a, b, {
        (Bool, Bool): bool,
        (Nat, Nat): int
    })
    handlers = {
        'AND': lambda x: x[0] & x[1],
        'OR': lambda x: x[0] | x[1],
        'XOR': lambda x: x[0] ^ x[1]
    }
    res = type(a)(handlers[prim]((val_type(a), val_type(b))))
    return stack.ins(res, annots=annots)


@instruction('NOT')
def do_not(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, [Nat, Int, Bool])
    if type(top) in [Nat, Int]:
        res = Int(~int(top))
    elif type(top) == Bool:
        res = Bool(not bool(top))
    else:
        assert False
    return stack.ins(res, annots=annots)


@instruction('BLAKE2B')
def do_blake2b(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Bytes)
    res = Bytes(blake2b_32(bytes(top)).digest())
    return stack.ins(res, annots=annots)


@instruction('CHECK_SIGNATURE')
def do_check_sig(stack: Stack, prim, args, annots):
    pk, sig, msg = stack.pop3()
    assert_stack_type(pk, Key)
    assert_stack_type(sig, Signature)
    assert_stack_type(msg, Bytes)
    key = Key.from_encoded_key(str(pk))
    try:
        key.verify(signature=str(sig), message=bytes(msg))
    except:
        res = Bool(False)
    else:
        res = Bool(True)
    return stack.ins(res, annots=annots)


@instruction('HASH_KEY')
def do_hash_key(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Key)
    key = Key.from_encoded_key(str(top))
    res = KeyHash(key.public_key_hash())
    return stack.ins(res, annots=annots)


@instruction(['SHA256', 'SHA512'])
def do_sha(stack: Stack, prim, args, annots):
    top = stack.pop()
    assert_stack_type(top, Bytes)
    handlers = {
        'SHA256': lambda x: sha256(x).digest(),
        'SHA512': lambda x: sha512(x).digest(),
    }
    res = Bytes(handlers[prim](bytes(top)))
    return stack.ins(res, annots=annots)
