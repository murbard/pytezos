from pytezos.michelson.forge import forge_micheline
from pytezos.repl.control import instruction
from pytezos.repl.stack import Stack
from pytezos.repl.types import assert_type, Option, Pair, String, Bytes, List, BigMap, Map, Set, Or, Bool, Nat, \
    Unit, StackItem


@instruction(['CAR', 'CDR'])
def do_car(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Pair)
    handlers = {
        'CAR': lambda x: x[0],
        'CDR': lambda x: x[1]
    }
    res = handlers[prim](top.value)
    stack.ins(res)


@instruction('CONCAT')
def do_concat(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, [String, Bytes, List])
    if type(top) in [String, Bytes]:
        second = stack.pop()
        assert_type(second, type(top))
        res_type = type(top)
        res = res_type(top.value + second.value)
    elif type(top) == List:
        val_type = top.val_type()
        delimiter = val_type()
        assert_type(delimiter, [String, Bytes])
        res = val_type(delimiter.join(top.value))
    else:
        assert False
    stack.ins(res)


@instruction('CONS')
def do_cons(stack: Stack, prim, args):
    elt, lst = stack.pop2()
    assert_type(lst, List)
    lst.assert_val_type(elt)
    res = elt + lst
    stack.ins(res)


@instruction('EMPTY_BIG_MAP', args_len=2)
def do_empty_big_map(stack: Stack, prim, args):
    res = BigMap.empty(k_type_expr=args[0], v_type_expr=args[1])
    stack.ins(res)


@instruction('EMPTY_MAP', args_len=2)
def do_empty_map(stack: Stack, prim, args):
    res = Map.empty(k_type_expr=args[0], v_type_expr=args[1])
    stack.ins(res)


@instruction('EMPTY_SET', args_len=1)
def do_empty_set(stack: Stack, prim, args):
    res = Set.empty(k_type_expr=args[0])
    stack.ins(res)


@instruction('GET')
def do_get(stack: Stack, prim, args):
    key, bmp = stack.pop2()
    assert_type(bmp, [Map, BigMap])
    res = bmp[key]
    stack.ins(res)


@instruction(['LEFT', 'RIGHT'], args_len=1)
def do_left(stack: Stack, prim, args):
    top = stack.pop()
    if prim == 'LEFT':
        res = Or.left(type_expr=args[0], item=top)
    else:
        res = Or.right(type_expr=args[0], item=top)
    stack.ins(res)


@instruction('MEM')
def do_mem(stack: Stack, prim, args):
    key, container = stack.pop2()
    assert_type(container, [Set, Map, BigMap])
    container.assert_key_type(key)
    res = Bool(key.value in container.value)
    stack.ins(res)


@instruction('NIL', args_len=1)
def do_nil(stack: Stack, prim, args):
    nil = List.empty(args[0])
    stack.ins(nil)


@instruction('NONE', args_len=1)
def do_none(stack: Stack, prim, args):
    none = Option.none(args[0])
    stack.ins(none)


@instruction('PACK')
def do_pack(stack: Stack, prim, args):
    top = stack.pop()
    res = Bytes(forge_micheline(top.val_node))
    stack.ins(res)


@instruction('PAIR')
def do_pair(stack: Stack, prim, args):
    left, right = stack.pop2()
    res = Pair.new(left, right)
    stack.ins(res)


@instruction('SIZE')
def do_size(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, [String, Bytes, List, Set, Map])
    res = Nat(len(top.value))
    stack.ins(res)


@instruction('SLICE')
def do_slice(stack: Stack, prim, args):
    offset, length, s = stack.pop3()
    assert_type(s, [String, Bytes])
    res_type = type(s)
    if offset + length < len(s.value):
        sls = s.value[offset:offset + length]
        res = Option.some(res_type(sls))
    else:
        res = Option.none(res_type().type_expr)
    stack.ins(res)


@instruction('SOME')
def do_some(stack: Stack, prim, args):
    top = stack.pop()
    res = Option.some(top)
    stack.ins(res)


@instruction('UNIT')
def do_unit(stack: Stack, prim, args):
    stack.ins(Unit())


@instruction('UNPACK', args_len=1)
def do_unpack(stack: Stack, prim, args):
    top = stack.pop()
    assert_type(top, Bytes)
    # TODO: parse micheline
    res = StackItem.parse(type_expr=args[0], val_expr=None)
    stack.ins(res)


@instruction('UPDATE')
def do_update(stack: Stack, prim, args):
    key, val, container = stack.pop3()
    assert_type(container, [Set, Map, BigMap])
    container.assert_key_type(key)

    if type(container) == Set:
        assert_type(val, Bool)
        if val:
            container.value.add(key)  # TODO
        else:
            container.value.remove(key)  # TODO
    else:
        assert_type(val, Option)
        if val.value is None:
            if key in container.value:
                del container.value[key]  # TODO
        else:
            container.assert_val_type(val.value)
            container.value[key] = val.value  # TODO

    stack.ins(container)
