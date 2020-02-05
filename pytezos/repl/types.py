import calendar
from pprint import pformat
from datetime import datetime

import pytezos.encoding as encoding

COMPARABLE = 1
PASSABLE = 2
STORABLE = 4
PUSHABLE = 8
PACKABLE = 16


def assert_type(value, py_type):
    assert type(value) == py_type, f'Expected {py_type}, got {type(value)}'


def assert_args_len(node, args_len: int):
    node_args = node.get('args', [])
    node_args_len = len(node_args)
    assert node_args_len == args_len, f'Expected {args_len} arg(s), got {node_args_len}: {pformat(node)}'


def check_prim(val_expr, prim, args_len: int) -> bool:
    assert_type(val_expr, dict)
    return val_expr.get('prim') == prim \
        and len(val_expr.get('args', [])) == args_len


def assert_prim(val_expr, prim, args_len: int):
    assert check_prim(val_expr, prim, args_len), f'Expected {prim} ({args_len} args): {pformat(val_expr)}'


def check_core(val_expr, core_type) -> bool:
    assert_type(val_expr, dict)
    assert len(val_expr.keys()) == 1, f'Expected single key, got {val_expr.keys()}: {pformat(val_expr)}'
    return next(iter(val_expr)) == core_type


def assert_core_type(val_expr, core_type):
    assert check_core(val_expr, core_type), f'Expected {core_type}: {pformat(val_expr)}'


def assert_item_type(item: 'StackItem', item_type):
    if not isinstance(item_type, list):
        item_type = [item_type]
    assert type(item) in item_type, f'Expected {item_type}, got {type(item)}'


class StackItem:
    prim = ''
    flags = 0
    __cls__ = {}

    def __init__(self, value, type_expr, val_expr):
        self.value = value
        self.type_expr = type_expr
        self.val_expr = val_expr

    @staticmethod
    def dispatch(type_expr):
        assert_type(type_expr, dict)
        prim = type_expr.get('prim')
        assert prim in StackItem.__cls__, f'Unknown primitive {prim}: {pformat(type_expr)}'
        item_class, args_len = StackItem.__cls__[type_expr['prim']]
        assert_args_len(type_expr, args_len)
        return item_class

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        item_class = StackItem.dispatch(type_expr)
        return item_class.from_expr(type_expr, val_expr)

    @classmethod
    def __init_subclass__(cls, prim='', args_len=0, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__cls__[prim] = cls, args_len
        cls.prim = prim

    def is_comparable(self) -> bool:
        return self.flags & COMPARABLE != 0

    def is_pushable(self) -> bool:
        return self.flags & PUSHABLE != 0

    def has_big_map(self) -> bool:
        return any(map(
            lambda x: x == BigMap or x.has_big_map(),
            map(StackItem.dispatch, self.type_expr['args'])))


class String(StackItem, prim='string'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, value='', type_expr=None, val_expr=None):
        assert_type(value, str)
        super(String, self).__init__(value,
                                     type_expr or {'prim': self.prim},
                                     val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core_type(val_expr, 'string')
        return cls(val_expr['string'], type_expr, val_expr)


class Int(StackItem, prim='int'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, value=0, type_expr=None, val_expr=None):
        assert_type(value, int)
        super(Int, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'int': str(value)})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core_type(val_expr, 'int')
        return cls(int(val_expr['int']), type_expr, val_expr)


class Bytes(StackItem, prim='bytes'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, value=b'', type_expr=None, val_expr=None):
        assert_type(value, bytes)
        super(Bytes, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'bytes': value.hex()})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core_type(val_expr, 'bytes')
        return cls(bytes.fromhex(val_expr['bytes']), type_expr, val_expr)


class Nat(Int, prim='nat'):
    pass


class Bool(StackItem, prim='bool'):

    def __init__(self, value=False, type_expr=None, val_expr=None):
        assert_type(value, bool)
        super(Bool, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'int': str(value)})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_prim(val_expr, prim='False', args_len=0):
            value = False
        elif check_prim(val_expr, prim='True', args_len=0):
            value = True
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(value, type_expr, val_expr)


class Unit(StackItem, prim='unit'):

    def __init__(self, value=None, type_expr=None, val_expr=None):
        super(Unit, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'prim': 'Unit'})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_prim(val_expr, prim='Unit', args_len=0)
        return cls(None, type_expr, val_expr)


class List(StackItem, prim='list', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_type(val_expr, list)
        elt_cls = StackItem.dispatch(type_expr['args'][0])
        value = [elt_cls.from_expr(type_expr['args'][0], item) for item in val_expr]
        return cls(value, type_expr, val_expr)

    @classmethod
    def empty(cls, e_type_expr):
        return cls(type_expr={'prim': cls.prim, 'args': [e_type_expr]}, val_expr=[], value=[])

    def val_type(self):
        return StackItem.dispatch(self.type_expr['args'][0])

    def assert_val_type(self, item: StackItem):
        cty = self.type_expr['args'][0]
        assert item.type_expr == cty, f'Expected {pformat(cty)}, got {pformat(item.type_expr)}'


class Pair(StackItem, prim='pair', args_len=1):

    def __init__(self, left, right, type_expr=None, val_expr=None):
        super(Pair, self).__init__((left, right),
                                   type_expr or {'prim': self.prim, 'args': [left.type_expr, right.type_expr]},
                                   val_expr or {'prim': 'Pair', 'args': [left.val_expr, right.val_expr]})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_prim(val_expr, prim='Pair', args_len=2)
        args = [StackItem.from_expr(type_expr['args'][i], val_expr['args'][i]) for i in [0, 1]]
        return cls(*args, type_expr, val_expr)

    def is_comparable(self):
        left_cls, right_cls = list(map(StackItem.dispatch, self.type_expr['args']))
        return type(left_cls) != Pair and right_cls.is_comparable()


class Option(StackItem, prim='option', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_prim(val_expr, prim='None', args_len=0):
            value = None
        elif check_prim(val_expr, prim='Some', args_len=1):
            value = StackItem.from_expr(type_expr['args'][0], val_expr['args'][0])
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(value, type_expr, val_expr)

    @classmethod
    def some(cls, item: StackItem):
        return cls(type_expr={'prim': cls.prim, 'args': [item.type_expr]},
                   val_expr={'prim': 'Some', 'args': [item.val_expr]},
                   value=item)

    @classmethod
    def none(cls, type_expr):
        return cls(type_expr={'prim': cls.prim, 'args': [type_expr]},
                   val_expr={'prim': 'None'},
                   value=None)


class Or(StackItem, prim='or', args_len=2):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_prim(val_expr, prim='Left', args_len=1):
            idx = 0
        elif check_prim(val_expr, prim='Right', args_len=1):
            idx = 1
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        value = StackItem.from_expr(type_expr['args'][idx], val_expr['args'][0])
        return cls(value, type_expr, val_expr)

    @classmethod
    def left(cls, type_expr, item: StackItem):
        cty = type_expr['args'][0]
        assert cty == item.type_expr, f'Expected {pformat(cty)}, got {pformat(item.type_expr)}'
        return cls(type_expr=type_expr,
                   val_expr={'prim': 'Left', 'args': [item.val_expr]},
                   value=item)

    @classmethod
    def right(cls, type_expr, item: StackItem):
        cty = type_expr['args'][1]
        assert cty == item.type_expr, f'Expected {pformat(cty)}, got {pformat(item.type_expr)}'
        return cls(type_expr=type_expr,
                   val_expr={'prim': 'Right', 'args': [item.val_expr]},
                   value=item)


class Set(StackItem, prim='set', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_type(val_expr, list)
        elt_cls = StackItem.dispatch(type_expr['args'][0])
        assert elt_cls.is_comparable(), f'Expected comparable item type: {pformat(type_expr)}'
        value = {elt_cls.from_expr(type_expr['args'][0], item) for item in val_expr}
        assert len(value) == len(val_expr), f'Duplicate elements found: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)

    @classmethod
    def empty(cls, e_type_expr):
        assert StackItem.dispatch(e_type_expr).is_comparable(), f'Item type is not comparable: {pformat(e_type_expr)}'
        return cls(type_expr={'prim': cls.prim, 'args': [e_type_expr]}, val_expr=[], value=set())

    def assert_key_type(self, item: StackItem):
        cty = self.type_expr['args'][0]
        assert item.type_expr == cty, f'Expected {pformat(cty)}, got {pformat(item.type_expr)}'


class Map(StackItem, prim='map', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_type(val_expr, list)
        k_cls, v_cls = list(map(StackItem.dispatch, type_expr['args']))
        assert k_cls.is_comparable(), f'Expected comparable key type: {pformat(type_expr)}'

        def parse_elt(elt):
            assert_prim(elt, prim='Elt', args_len=2)
            return k_cls(type_expr['args'][0], elt['args'][0]), \
                   v_cls(type_expr['args'][1], elt['args'][1])

        value = dict(map(parse_elt, val_expr))
        assert len(value) == len(val_expr), f'Duplicate keys found: {pformat(val_expr)}'
        return cls(value, type_expr, val_expr)

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert StackItem.dispatch(k_type_expr).is_comparable(), f'Key type is not comparable: {pformat(k_type_expr)}'
        return cls(type_expr={'prim': cls.prim, 'args': [k_type_expr, v_type_expr]}, val_expr=[], value=dict())

    def val_type_expr(self):
        return self.type_expr['args'][1]

    def assert_key_type(self, item: StackItem):
        kty = self.type_expr['args'][0]
        assert item.type_expr == kty, f'Expected {pformat(kty)}, got {pformat(item.type_expr)}'

    def assert_val_type(self, item: StackItem):
        vty = self.type_expr['args'][1]
        assert item.type_expr == vty, f'Expected {pformat(vty)}, got {pformat(item.type_expr)}'


class BigMap(Map, prim='big_map', args_len=1):

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert not StackItem.dispatch(v_type_expr).has_big_map(), f'Cannot contain big map: {pformat(v_type_expr)}'
        return Map.empty(k_type_expr, v_type_expr)


class Timestamp(StackItem, prim='timestamp'):

    def __init__(self, value=0, type_expr=None, val_expr=None):
        assert_type(value, int)
        super(Timestamp, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'int': str(value)})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, 'int'):
            value = int(val_expr['int'])
        elif check_core(val_expr, 'string'):
            dt = datetime.strptime(val_expr['string'], '%Y-%m-%dT%H:%M:%SZ')
            value = calendar.timegm(dt.utctimetuple())
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(value, type_expr, val_expr)


class Mutez(Nat, prim='mutez'):
    pass


class Address(StackItem, prim='address'):

    def __init__(self, value, type_expr=None, val_expr=None):
        assert_type(value, str)
        super(Address, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, core_type='string'):
            value = val_expr['string']
        elif check_core(val_expr, core_type='bytes'):
            value = encoding.parse_address(bytes.fromhex(val_expr['bytes']))
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)


class Contract(Address, prim='contract'):
    pass


class Operation(StackItem, prim='operation'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        raise NotImplementedError


class Key(StackItem, prim='key'):

    def __init__(self, value, type_expr=None, val_expr=None):
        assert_type(value, str)
        super(Key, self).__init__(value, type_expr or {'prim': self.prim}, val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, core_type='string'):
            value = val_expr['string']
        elif check_core(val_expr, core_type='bytes'):
            value = encoding.parse_public_key(bytes.fromhex(val_expr['bytes']))
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)


class KeyHash(Address, prim='key_hash'):
    pass


class Signature(String, prim='signature'):
    pass


class ChainID(String, prim='chain_id'):
    pass


class Lambda(StackItem, prim='lambda'):  # TODO:
    pass
