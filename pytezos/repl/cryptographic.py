from hashlib import sha256, sha512

from pytezos.crypto import blake2b_32, Key
from pytezos.repl.instructions import primitive
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_item_type, Bytes, Key, Signature, Bool, KeyHash


@primitive('BLAKE2B')
def do_blake2b(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Bytes)
    res = Bytes(blake2b_32(top.value).digest())
    stack.ins(res)


@primitive('CHECK_SIGNATURE')
def do_check_sig(stack: Stack, prim, args):
    pk, sig, msg = stack.pop3()
    assert_item_type(pk, Key)
    assert_item_type(sig, Signature)
    assert_item_type(msg, Bytes)
    key = Key.from_encoded_key(pk.value)
    try:
        key.verify(signature=sig.value, message=msg.value)
    except:
        res = Bool(False)
    else:
        res = Bool(True)
    stack.ins(res)


@primitive('HASH_KEY')
def do_hash_key(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Key)
    key = Key.from_encoded_key(top.value)
    res = KeyHash(key.public_key_hash())
    stack.ins(res)


@primitive('(SHA256|SHA512)')
def do_sha(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Bytes)
    res_mapping = {
        'SHA256': lambda x: sha256(x).digest(),
        'SHA512': lambda x: sha512(x).digest(),
    }
    res = Bytes(res_mapping[prim](top.value))
    stack.ins(res)
