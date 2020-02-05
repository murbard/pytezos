from pytezos.michelson.forge import forge_micheline
from pytezos.repl.instructions import primitive
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_item_type, Option, Pair, String, Bytes, List, BigMap, Map, Set, Or, Bool, Nat, \
    Unit, StackItem


@primitive('(CAR|CDR')
def do_car(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Pair)
    res_mapping = {
        'CAR': lambda x: x[0],
        'CDR': lambda x: x[1]
    }
    res = res_mapping[prim](top.value)
    stack.ins(res)


@primitive('CONCAT')
def do_concat(stack: Stack, prim, args):
    top = stack.pop()
    res_cls = type(top)
    if res_cls in [String, Bytes]:
        second = stack.pop()
        assert_item_type(second, res_cls)
        res = res_cls(top.value + second.value)
    else:
        assert_item_type(top, List)
        elt_cls = top.val_type()
        if elt_cls == String:
            res = String(''.join(top.value))
        elif elt_cls == Bytes:
            res = Bytes(b''.join(top.value))
        else:
            assert False, f'Unexpected element type: {elt_cls}'
    stack.ins(res)


@primitive('CONS')
def do_cons(stack: Stack, prim, args):
    elt, lst = stack.pop2()
    assert_item_type(lst, List)
    lst.assert_val_type(elt)
    lst.value.insert(0, elt)
    stack.ins(lst)


@primitive('EMPTY_BIG_MAP', args_len=2)
def do_empty_big_map(stack: Stack, prim, args):
    res = BigMap.empty(k_type_expr=args[0], v_type_expr=args[1])
    stack.ins(res)


@primitive('EMPTY_MAP', args_len=2)
def do_empty_map(stack: Stack, prim, args):
    res = Map.empty(k_type_expr=args[0], v_type_expr=args[1])
    stack.ins(res)


@primitive('EMPTY_SET', args_len=1)
def do_empty_set(stack: Stack, prim, args):
    res = Set.empty(e_type_expr=args[0])
    stack.ins(res)


@primitive('GET')
def do_get(stack: Stack, prim, args):
    key, bmp = stack.pop2()
    assert_item_type(bmp, [Map, BigMap])
    bmp.assert_key_type(key)
    if key in bmp.value:
        res = Option.some(bmp.value[key])
    else:
        res = Option.none(bmp.val_type_expr())
    stack.ins(res)


@primitive('(LEFT|RIGHT)', args_len=1)
def do_left(stack: Stack, prim, args):
    top = stack.pop()
    if prim == 'LEFT':
        res = Or.left(type_expr=args[0], item=top)
    else:
        res = Or.right(type_expr=args[0], item=top)
    stack.ins(res)


@primitive('MAP', args_len=1)
def do_map(stack: Stack, prim, args):
    coll = stack.pop()
    if type(coll) == List:
        res = list()
        for item in coll.value:
            stack.ins(item)
            # TODO: execute args[0]
            val = stack.pop()
            coll.assert_val_type(val)
            res.append(val)
    elif type(coll) == Map:
        res = dict()
        for key, value in coll.value.items():
            stack.ins(Pair(key, value))
            # TODO: execute args[0]
            val = stack.pop()
            coll.assert_val_type(val)
            res[key] = res
    else:
        assert False, f'Unexpected type: {type(coll)}'
    coll.value = res
    stack.ins(coll)


@primitive('MEM')
def do_mem(stack: Stack, prim, args):
    key, coll = stack.pop2()
    assert_item_type(coll, [Set, Map, BigMap])
    coll.assert_key_type(key)
    res = Bool(key in coll.value)
    stack.ins(res)


@primitive('NIL', args_len=1)
def do_nil(stack: Stack, prim, args):
    nil = List.empty(args[0])
    stack.ins(nil)


@primitive('NONE', args_len=1)
def do_none(stack: Stack, prim, args):
    none = Option.none(args[0])
    stack.ins(none)


@primitive('PACK')
def do_pack(stack: Stack, prim, args):
    top = stack.pop()
    res = Bytes(forge_micheline(top.val_node))
    stack.ins(res)


@primitive('PAIR')
def do_pair(stack: Stack, prim, args):
    left, right = stack.pop2()
    res = Pair(left, right)
    stack.ins(res)


@primitive('SIZE')
def do_size(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, [String, Bytes, List, Set, Map])
    res = Nat(len(top.value))
    stack.ins(res)


@primitive('SLICE')
def do_slice(stack: Stack, prim, args):
    offset, length, s = stack.pop3()
    assert_item_type(s, [String, Bytes])
    res_cls = type(s)
    if offset + length < len(s.value):
        sls = s.value[offset:offset + length]
        res = Option.some(res_cls(sls))
    else:
        res = Option.none(res_cls().type_expr)
    stack.ins(res)


@primitive('SOME')
def do_some(stack: Stack, prim, args):
    top = stack.pop()
    res = Option.some(top)
    stack.ins(res)


@primitive('UNIT')
def do_unit(stack: Stack, prim, args):
    stack.ins(Unit())


@primitive('UNPACK', args_len=1)
def do_unpack(stack: Stack, prim, args):
    top = stack.pop()
    assert_item_type(top, Bytes)
    # TODO: parse micheline
    res = StackItem.from_expr(type_expr=args[0], val_expr=None)
    stack.ins(res)


@primitive('UPDATE')
def do_update(stack: Stack, prim, args):
    key, val, coll = stack.pop3()
    assert_item_type(coll, [Set, Map, BigMap])
    coll.assert_key_type(key)

    if type(coll) == Set:
        assert_item_type(val, Bool)
        if val:
            coll.value.add(key)
        else:
            coll.value.remove(key)
    else:
        assert_item_type(val, Option)
        if val.value is None:
            if key in coll.value:
                del coll.value[key]
        else:
            coll.assert_val_type(val.value)
            coll.value[key] = val.value

    stack.ins(coll)
