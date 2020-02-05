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


def assert_core(val_expr, core_type):
    assert check_core(val_expr, core_type), f'Expected {core_type}: {pformat(val_expr)}'


def assert_item(item: 'StackItem', item_type):
    assert type(item) == item_type, f'Expected {item_type}, got {type(item)}'


class StackItem:
    prim = ''
    flags = 0
    __cls__ = {}

    def __init__(self, type_expr, val_expr, value):
        self.type_expr = type_expr
        self.val_expr = val_expr
        self.value = value

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
    def from_val(cls, value):
        raise NotImplementedError

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

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core(val_expr, 'string')
        return cls(type_expr, val_expr, val_expr['string'])

    @classmethod
    def from_val(cls, value):
        assert_type(value, str)
        return cls({'prim': cls.prim}, {'string': value}, value)


class Int(StackItem, prim='int'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core(val_expr, 'int')
        return cls(type_expr, val_expr, int(val_expr['int']))

    @classmethod
    def from_val(cls, value):
        assert_type(value, int)
        return cls({'prim': cls.prim}, {'int': str(value)}, value)


class Bytes(StackItem, prim='bytes'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_core(val_expr, 'bytes')
        return cls(type_expr, val_expr, bytes.fromhex(val_expr['bytes']))

    @classmethod
    def from_val(cls, value):
        assert_type(value, bytes)
        return cls({'prim': cls.prim}, {'bytes': value.hex()}, value)


class Nat(Int, prim='nat'):
    pass


class Bool(StackItem, prim='bool'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_prim(val_expr, prim='False', args_len=0):
            value = False
        elif check_prim(val_expr, prim='True', args_len=0):
            value = True
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        assert_type(value, bool)
        return cls({'prim': cls.prim}, {'prim': str(value)}, value)


class Unit(StackItem, prim='unit'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_prim(val_expr, prim='Unit', args_len=0)
        return cls(type_expr, val_expr, None)

    @classmethod
    def from_val(cls, value):
        return cls({'prim': cls.prim}, {'prim': 'Unit'}, None)


class List(StackItem, prim='list', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_type(val_expr, list)
        elt_cls = StackItem.dispatch(type_expr['args'][0])
        value = [elt_cls.from_expr(type_expr['args'][0], item) for item in val_expr]
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        assert_type(value, list)
        assert len(value) > 0, f'Cannot instantiate from an empty list (no type info)'
        type_expr = value[0].type_expr
        assert all(map(lambda x: x.type_expr == type_expr, value)), f'List must be homogeneous'
        return cls(type_expr={'prim': cls.prim, 'args': [type_expr]},
                   val_expr=list(map(lambda x: x.val_expr, value)),
                   value=value)

    @classmethod
    def empty(cls, default: StackItem):
        return cls(type_expr={'prim': cls.prim, 'args': [default.type_expr]}, val_expr=[], value=[])


class Pair(StackItem, prim='pair', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert_prim(val_expr, prim='Pair', args_len=2)
        value = tuple(StackItem.from_expr(type_expr['args'][i], val_expr['args'][i]) for i in [0, 1])
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        assert_type(value, tuple)
        left, right = value
        return cls(type_expr={'prim': cls.prim, 'args': [left.type_expr, right.type_expr]},
                   val_expr={'prim': 'Pair', 'args': [left.val_expr, right.val_expr]},
                   value=value)

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
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        assert isinstance(value, StackItem), f'Expected stack item, got {type(value)}'
        return cls(type_expr={'prim': cls.prim, 'args': [value.type_expr]},
                   val_expr={'prim': 'Some', 'args': [value.val_expr]},
                   value=value)

    @classmethod
    def none(cls, default: StackItem):
        return cls(type_expr={'prim': cls.prim, 'args': [default.type_expr]},
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
        return cls(type_expr, val_expr, value)


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
    def from_val(cls, value):
        assert_type(value, set)
        assert len(value) > 0, f'Cannot instantiate from an empty set (no type info)'
        type_expr = value[0].type_expr
        assert all(map(lambda x: x.type_expr == type_expr, value)), f'Set must be homogeneous'
        return cls(type_expr={'prim': cls.prim, 'args': [type_expr]},
                   val_expr=list(map(lambda x: x.val_expr, value)),
                   value=value)

    @classmethod
    def empty(cls, default: StackItem):
        return cls(type_expr={'prim': cls.prim, 'args': [default.type_expr]}, val_expr=[], value={})


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
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        assert_type(value, dict)
        assert len(value) > 0, f'Cannot instantiate from an empty dict (no type info)'

        items = list(value.items())  # TODO: sort keys
        k_type_expr, v_type_expr = list(map(lambda x: x.type_expr, items[0]))
        assert all(k.type_expr == k_type_expr and v.type_expr == v_type_expr for k, v in items), \
            f'Map must be homogeneous'

        def make_elt(item):
            return {'prim': 'Elt', 'args': list(map(lambda x: x.val_expr, item))}

        return cls(type_expr={'prim': cls.prim, 'args': [k_type_expr, v_type_expr]},
                   val_expr=list(map(make_elt, items)),
                   value=value)


class BigMap(Map, prim='big_map', args_len=1):
    pass


class Timestamp(StackItem, prim='timestamp'):

    @staticmethod
    def parse_utc(value) -> int:
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return calendar.timegm(dt.utctimetuple())

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, 'int'):
            value = int(val_expr['int'])
        elif check_core(val_expr, 'string'):
            value = Timestamp.parse_utc(val_expr['string'])
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        if isinstance(value, int):
            return cls({'prim': cls.prim}, {'int': str(value)}, value)
        elif isinstance(value, str):
            return cls({'prim': cls.prim}, {'string': value}, Timestamp.parse_utc(value))
        else:
            assert False, f'Unexpected type {type(value)}'


class Mutez(Nat, prim='mutez'):
    pass


class Address(StackItem, prim='address'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, core_type='string'):
            value = val_expr['string']
        elif check_core(val_expr, core_type='bytes'):
            value = encoding.parse_address(bytes.fromhex(val_expr['bytes']))
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        if isinstance(value, bytes):
            return cls({'prim': cls.prim}, {'bytes': value.hex()}, encoding.parse_address(value))
        elif isinstance(value, str):
            return cls({'prim': cls.prim}, {'string': value}, value)
        else:
            assert False, f'Unexpected type {type(value)}'


class Contract(Address, prim='contract'):
    pass


class Operation(StackItem, prim='operation'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        raise NotImplementedError


class Key(StackItem, prim='key'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        if check_core(val_expr, core_type='string'):
            value = val_expr['string']
        elif check_core(val_expr, core_type='bytes'):
            value = encoding.parse_public_key(bytes.fromhex(val_expr['bytes']))
        else:
            assert False, f'Expected {pformat(type_expr)}: {pformat(val_expr)}'
        return cls(type_expr, val_expr, value)

    @classmethod
    def from_val(cls, value):
        if isinstance(value, bytes):
            return cls({'prim': cls.prim}, {'bytes': value.hex()}, encoding.parse_public_key(value))
        elif isinstance(value, str):
            return cls({'prim': cls.prim}, {'string': value}, value)
        else:
            assert False, f'Unexpected type {type(value)}'


class KeyHash(Address, prim='key_hash'):
    pass


class Signature(String, prim='signature'):
    pass


class ChainID(String, prim='chain_id'):
    pass


class Lambda(StackItem, prim='lambda'):
    pass
