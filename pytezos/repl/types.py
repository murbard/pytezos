import calendar
from pprint import pformat
from datetime import datetime

from pytezos.michelson.converter import micheline_to_michelson
from pytezos.repl.typechecker import parse_prim_expr, get_prim_args, dispatch_prim_map, assert_expr_equal, \
    assert_comparable, assert_big_map_val, get_core_val, dispatch_core_map
import pytezos.encoding as encoding


def assert_type(item: 'StackItem', item_type):
    if not isinstance(item_type, list):
        item_type = [item_type]
    expected = ' or '.join(map(lambda x: x.__name__, item_type))
    assert type(item) in item_type, f'expected {expected}, got {type(item).__name__}: {item}'


class StackItem:
    prim = ''
    __cls__ = {}

    def __init__(self, value, type_expr, val_expr):
        self.value = value
        self.type_expr = type_expr
        self.val_expr = val_expr

    @staticmethod
    def dispatch(type_expr):
        prim, args = parse_prim_expr(type_expr)
        assert prim in StackItem.__cls__, f'{prim}: unknown type primitive'
        item_cls, args_len = StackItem.__cls__[type_expr['prim']]
        assert len(args) == args_len, f'{prim}: expected {args_len} arg(s), got {len(args)}'
        return item_cls

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        return StackItem.dispatch(type_expr).from_expr(type_expr, val_expr)

    @classmethod
    def __init_subclass__(cls, prim='', args_len=0, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__cls__[prim] = cls, args_len
        cls.prim = prim

    def __hash__(self):
        return hash(self.val_expr)

    def __repr__(self):
        return micheline_to_michelson(self.val_expr)

    def type(self):
        return micheline_to_michelson(self.type_expr)

    def _arg_type(self, arg_idx: int):
        return StackItem.dispatch(self.type_expr['args'][arg_idx])

    def _arg_type_expr(self, arg_idx):
        return self.type_expr['args'][arg_idx]


class String(StackItem, prim='string'):

    def __init__(self, value='', type_expr=None, val_expr=None):
        assert isinstance(value, str)
        super(String, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        value = get_core_val(val_expr, core_type='string')
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Int(StackItem, prim='int'):

    def __init__(self, value=0, type_expr=None, val_expr=None):
        assert isinstance(value, int)
        super(Int, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'int': str(value)})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        value = int(get_core_val(val_expr, core_type='int'))
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Bytes(StackItem, prim='bytes'):

    def __init__(self, value=b'', type_expr=None, val_expr=None):
        assert isinstance(value, bytes)
        super(Bytes, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'bytes': value.hex()})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        value = bytes.fromhex(get_core_val(val_expr, core_type='bytes'))
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Nat(Int, prim='nat'):
    pass


class Bool(StackItem, prim='bool'):

    def __init__(self, value=False, type_expr=None, val_expr=None):
        assert isinstance(value, bool)
        super(Bool, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'int': str(value)})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            ('False', 0): False,
            ('True', 0): True
        }
        value = dispatch_prim_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Unit(StackItem, prim='unit'):

    def __init__(self, value=None, type_expr=None, val_expr=None):
        super(Unit, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'prim': 'Unit'})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        _ = get_prim_args(val_expr, prim='Unit', args_len=0)
        return cls(value=None, type_expr=type_expr, val_expr=val_expr)


class List(StackItem, prim='list', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert isinstance(val_expr, list)
        val_cls = StackItem.dispatch(type_expr['args'][0])
        value = [val_cls.from_expr(type_expr['args'][0], item) for item in val_expr]
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)

    @classmethod
    def empty(cls, e_type_expr):
        return cls(value=[],
                   type_expr={'prim': cls.prim, 'args': [e_type_expr]},
                   val_expr=[])

    def val_type(self):
        return StackItem.dispatch(self.type_expr['args'][0])

    def assert_val_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)


class Pair(StackItem, prim='pair', args_len=2):

    def __init__(self, left, right, type_expr=None, val_expr=None):
        assert isinstance(left, StackItem)
        assert isinstance(right, StackItem)
        super(Pair, self).__init__(
            value=(left, right),
            type_expr=type_expr or {'prim': self.prim, 'args': [left.type_expr, right.type_expr]},
            val_expr=val_expr or {'prim': 'Pair', 'args': [left.val_expr, right.val_expr]})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        args = get_prim_args(val_expr, prim='Pair', args_len=2)
        left, right = [StackItem.from_expr(type_expr['args'][i], args[i]) for i in [0, 1]]
        return cls(left=left, right=right, type_expr=type_expr, val_expr=val_expr)

    def is_comparable(self):
        left_cls, right_cls = list(map(StackItem.dispatch, self.type_expr['args']))
        return type(left_cls) != Pair and right_cls.is_comparable()


class Option(StackItem, prim='option', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            ('None', 0): None,
            ('Some', 1): lambda x: StackItem.from_expr(type_expr['args'][0], x[0])
        }
        value = dispatch_prim_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)

    @classmethod
    def some(cls, item: StackItem):
        return cls(value=item,
                   type_expr={'prim': cls.prim, 'args': [item.type_expr]},
                   val_expr={'prim': 'Some', 'args': [item.val_expr]})

    @classmethod
    def none(cls, type_expr):
        return cls(value=None,
                   type_expr={'prim': cls.prim, 'args': [type_expr]},
                   val_expr={'prim': 'None'})


class Or(StackItem, prim='or', args_len=2):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            ('Left', 1): lambda x: StackItem.from_expr(type_expr=type_expr['args'][0], val_expr=x[0]),
            ('Right', 1): lambda x: StackItem.from_expr(type_expr=type_expr['args'][1], val_expr=x[0])
        }
        value = dispatch_prim_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)

    @classmethod
    def left(cls, type_expr, item: StackItem):
        assert_expr_equal(type_expr['args'][0], item.type_expr)
        return cls(value=item,
                   type_expr=type_expr,
                   val_expr={'prim': 'Left', 'args': [item.val_expr]})

    @classmethod
    def right(cls, type_expr, item: StackItem):
        assert_expr_equal(type_expr['args'][1], item.type_expr)
        return cls(value=item,
                   type_expr=type_expr,
                   val_expr={'prim': 'Right', 'args': [item.val_expr]})

    def is_left(self):
        prim, _ = parse_prim_expr(self.val_expr)
        return prim == 'Left'


class Set(StackItem, prim='set', args_len=1):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert isinstance(val_expr, list)
        assert_comparable(type_expr['args'][0])
        key_cls = StackItem.dispatch(type_expr['args'][0])
        value = {key_cls.from_expr(type_expr['args'][0], item) for item in val_expr}
        assert len(value) == len(val_expr), f'duplicate elements found: {pformat(val_expr)}'
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)

    @classmethod
    def empty(cls, k_type_expr):
        assert_comparable(k_type_expr)
        return cls(value=set(),
                   type_expr={'prim': cls.prim, 'args': [k_type_expr]},
                   val_expr=[])

    def assert_key_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)


class Map(StackItem, prim='map', args_len=2):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        assert isinstance(val_expr, list)
        assert_comparable(type_expr['args'][0])
        k_cls, v_cls = list(map(StackItem.dispatch, type_expr['args']))

        def parse_elt(elt):
            args = get_prim_args(elt, prim='Elt', args_len=2)
            return k_cls.from_expr(type_expr=type_expr['args'][0], val_expr=args[0]), \
                   v_cls.from_expr(type_expr=type_expr['args'][1], val_expr=args[1])

        value = dict(map(parse_elt, val_expr))
        assert len(value) == len(val_expr), f'duplicate keys found: {pformat(val_expr)}'
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert_comparable(k_type_expr)
        return cls(value=dict(),
                   type_expr={'prim': cls.prim, 'args': [k_type_expr, v_type_expr]},
                   val_expr=[])

    def val_type_expr(self):
        return self._arg_type_expr(1)

    def assert_key_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)

    def assert_val_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][1], item.type_expr)


class BigMap(Map, prim='big_map', args_len=1):

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert_big_map_val(v_type_expr)
        return super(BigMap, cls).empty(k_type_expr, v_type_expr)


class Timestamp(StackItem, prim='timestamp'):

    def __init__(self, value=0, type_expr=None, val_expr=None):
        assert isinstance(value, int)
        super(Timestamp, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'int': str(value)})

    @staticmethod
    def parse_utc(s):
        dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
        return calendar.timegm(dt.utctimetuple())

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            'int': lambda x: int(x),
            'string': lambda x: Timestamp.parse_utc(x)
        }
        value = dispatch_core_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Mutez(Nat, prim='mutez'):
    pass


class Address(StackItem, prim='address'):

    def __init__(self, value, type_expr=None, val_expr=None):
        assert isinstance(value, str)
        super(Address, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            'string': lambda x: x,
            'bytes': lambda x: encoding.parse_address(bytes.fromhex(x))
        }
        value = dispatch_core_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class Contract(Address, prim='contract'):
    pass


class Operation(StackItem, prim='operation'):

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        raise NotImplementedError


class Key(StackItem, prim='key'):

    def __init__(self, value, type_expr=None, val_expr=None):
        assert isinstance(value, str)
        super(Key, self).__init__(
            value=value,
            type_expr=type_expr or {'prim': self.prim},
            val_expr=val_expr or {'string': value})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        mapping = {
            'string': lambda x: x,
            'bytes': lambda x: encoding.parse_public_key(bytes.fromhex(x))
        }
        value = dispatch_core_map(val_expr, mapping)
        return cls(value=value, type_expr=type_expr, val_expr=val_expr)


class KeyHash(Address, prim='key_hash'):
    pass


class Signature(String, prim='signature'):
    pass


class ChainID(Bytes, prim='chain_id'):
    pass


class Lambda(StackItem, prim='lambda', args_len=2):

    def __init__(self, p_type_expr, r_type_expr, code):
        super(Lambda, self).__init__(
            value=code,
            type_expr={'prim': 'lambda', 'args': [p_type_expr, r_type_expr]},
            val_expr={'prim': 'Lambda', 'args': [code]})

    @classmethod
    def from_expr(cls, type_expr, val_expr):
        args = get_prim_args(val_expr, prim='Lambda', args_len=1)
        return cls(p_type_expr=type_expr['args'][0],
                   r_type_expr=type_expr['args'][1],
                   code=args[0])

    def assert_param_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)

    def assert_ret_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][1], item.type_expr)

    # def apply(self, item: StackItem):
    #     p_type_expr = self.type_expr['args'][0]
    #     assert_prim(p_type_expr, prim='pair', args_len=2)
    #     left_type_expr = p_type_expr['args'][0]
    #     assert left_type_expr == item.type_expr, f'Expected {pformat(left_type_expr)}, got {pformat(item.type_expr)}'
    #     push = {'prim': 'PUSH', 'args': [item.type_expr, item.val_expr]}
