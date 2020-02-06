from pprint import pformat

from pytezos.encoding import is_pkh
from pytezos.michelson.converter import micheline_to_michelson
from pytezos.repl.parser import parse_value, parse_prim_expr, assert_expr_equal, assert_comparable, \
    assert_big_map_val, expr_equal


def assert_stack_item(item: 'StackItem'):
    assert isinstance(item, StackItem), f'expected StackItem, got {type(item).__name__}'


def assert_type(item: 'StackItem', item_type):
    if not isinstance(item_type, list):
        item_type = [item_type]
    expected = ' or '.join(map(lambda x: x.__name__, item_type))
    assert type(item) in item_type, f'expected {expected}, got {type(item).__name__}: {item}'


class StackItem:
    prim = ''
    __cls__ = {}

    def __init__(self, *args, val_expr, type_expr):
        self.val_expr = val_expr
        self.type_expr = type_expr
        self.value = parse_value(val_expr, type_expr)

    @staticmethod
    def _get_type(type_expr):
        prim, args = parse_prim_expr(type_expr)
        assert prim in StackItem.__cls__, f'{prim}: unknown type primitive'
        item_cls, args_len = StackItem.__cls__[type_expr['prim']]
        assert len(args) == args_len, f'{prim}: expected {args_len} arg(s), got {len(args)}'
        return item_cls

    @staticmethod
    def parse(val_expr, type_expr):
        return StackItem._get_type(type_expr)(val_expr=val_expr, type_expr=type_expr)

    @classmethod
    def __init_subclass__(cls, prim='', args_len=0, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__cls__[prim] = cls, args_len
        cls.prim = prim

    def __repr__(self):
        return pformat(self.value)

    @property
    def val(self):
        return micheline_to_michelson(self.val_expr)

    @property
    def type(self):
        return micheline_to_michelson(self.type_expr)

    #
    # def _arg_type(self, arg_idx: int):
    #     return StackItem.dispatch(self.type_expr['args'][arg_idx])
    #
    # def _arg_type_expr(self, arg_idx):
    #     return self.type_expr['args'][arg_idx]


class String(StackItem, prim='string'):

    def __init__(self, value='', val_expr=None, type_expr=None):
        assert isinstance(value, str)
        super(String, self).__init__(
            val_expr=val_expr or {'string': value},
            type_expr=type_expr or {'prim': self.prim})


class Int(StackItem, prim='int'):

    def __init__(self, value=0, val_expr=None, type_expr=None):
        assert isinstance(value, int)
        super(Int, self).__init__(
            val_expr=val_expr or {'int': str(value)},
            type_expr=type_expr or {'prim': self.prim})


class Bytes(StackItem, prim='bytes'):

    def __init__(self, value=b'', type_expr=None, val_expr=None):
        assert isinstance(value, bytes)
        super(Bytes, self).__init__(
            val_expr=val_expr or {'bytes': value.hex()},
            type_expr=type_expr or {'prim': self.prim})


class Nat(Int, prim='nat'):

    def __init__(self, value=0, val_expr=None, type_expr=None):
        assert isinstance(value, int)
        assert value >= 0
        super(Nat, self).__init__(value, val_expr=val_expr, type_expr=type_expr)


class Bool(StackItem, prim='bool'):

    def __init__(self, value=False, val_expr=None, type_expr=None):
        assert isinstance(value, bool)
        super(Bool, self).__init__(
            val_expr=val_expr or {'int': str(value)},
            type_expr=type_expr or {'prim': self.prim})


class Unit(StackItem, prim='unit'):

    def __init__(self, val_expr=None, type_expr=None):
        super(Unit, self).__init__(
            val_expr=val_expr or {'prim': 'Unit'},
            type_expr=type_expr or {'prim': self.prim})


class List(StackItem, prim='list', args_len=1):

    def __iter__(self):
        val_type = self.val_type()
        for item in self.val_expr:
            yield val_type(val_expr=item, type_expr=self.type_expr['args'][0])

    def __radd__(self, item: StackItem) -> 'List':
        self.assert_val_type(item)
        return self.parse(val_expr=[item.val_expr] + self.val_expr, type_expr=self.type_expr)

    @classmethod
    def empty(cls, v_type_expr):
        return cls(val_expr=[], type_expr={'prim': cls.prim, 'args': [v_type_expr]})

    @classmethod
    def new(cls, items: list):
        assert isinstance(items, list) and len(items) > 0, f'expected non-empty list'
        val_expr = [assert_stack_item(x) or x.val_expr for x in items]
        return cls(val_expr=val_expr, type_expr={'prim': cls.prim, 'args': [items[0].type_expr]})

    def val_type(self):
        return self._get_type(self.type_expr['args'][0])

    def assert_val_type(self, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)


class Pair(StackItem, prim='pair', args_len=2):

    @classmethod
    def new(cls, left: StackItem, right: StackItem):
        assert_stack_item(left)
        assert_stack_item(right)
        return cls(
            type_expr={'prim': cls.prim, 'args': [left.type_expr, right.type_expr]},
            val_expr={'prim': 'Pair', 'args': [left.val_expr, right.val_expr]})


class Option(StackItem, prim='option', args_len=1):

    @classmethod
    def some(cls, item: StackItem):
        assert_stack_item(item)
        return cls(
            type_expr={'prim': cls.prim, 'args': [item.type_expr]},
            val_expr={'prim': 'Some', 'args': [item.val_expr]})

    @classmethod
    def none(cls, type_expr):
        return cls(
            type_expr={'prim': cls.prim, 'args': [type_expr]},
            val_expr={'prim': 'None'})


class Or(StackItem, prim='or', args_len=2):

    @classmethod
    def left(cls, type_expr, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(type_expr['args'][0], item.type_expr)
        return cls(type_expr=type_expr, val_expr={'prim': 'Left', 'args': [item.val_expr]})

    @classmethod
    def right(cls, type_expr, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(type_expr['args'][1], item.type_expr)
        return cls(type_expr=type_expr, val_expr={'prim': 'Right', 'args': [item.val_expr]})

    # def is_left(self):
    #     prim, _ = parse_prim_expr(self.val_expr)
    #     return prim == 'Left'


class Set(StackItem, prim='set', args_len=1):

    @classmethod
    def empty(cls, k_type_expr):
        assert_comparable(k_type_expr)
        return cls(type_expr={'prim': cls.prim, 'args': [k_type_expr]}, val_expr=[])

    def __iter__(self):
        key_type = self._get_type(self.type_expr['args'][0])
        for item in self.val_expr:
            yield key_type(val_expr=item, type_expr=self.type_expr['args'][0])

    def assert_key_type(self, item: StackItem):
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)


class Map(StackItem, prim='map', args_len=2):

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert_comparable(k_type_expr)
        return cls.parse(type_expr={'prim': cls.prim, 'args': [k_type_expr, v_type_expr]}, val_expr=[])

    @classmethod
    def new(cls, items: list):
        assert isinstance(items, list) and len(items) > 0, f'expected non-empty list'
        _ = [assert_stack_item(x) for kv in items for x in kv]
        val_expr = [(k.val_expr, v.val_expr) for k, v in items]
        k0, v0 = items[0]
        return cls(val_expr=val_expr, type_expr={'prim': cls.prim, 'args': [k0.type_expr, v0.type_expr]})

    def __iter__(self):
        kv_types = [self._get_type(self.type_expr['args'][i]) for i in [0, 1]]
        for elt in self.val_expr:
            yield tuple(
                kv_types[i](val_expr=elt['args'][i], type_expr=self.type_expr['args'][i])
                for i in [0, 1])

    def __getitem__(self, item: StackItem):
        self.assert_key_type(item)
        if item.value in self.value:
            val_expr = next(
                elt['args'][1]
                for elt in self.val_expr
                if expr_equal(elt['args'][0], item.val_expr))
            type_expr = self.type_expr['args'][1]
            val_type = self._get_type(type_expr)
            return Option.some(val_type(type_expr=type_expr, val_expr=val_expr))
        else:
            return Option.none(self.type_expr['args'][1])

    def assert_key_type(self, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)

    def assert_val_type(self, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(self.type_expr['args'][1], item.type_expr)


class BigMap(Map, prim='big_map', args_len=1):

    @classmethod
    def empty(cls, k_type_expr, v_type_expr):
        assert_big_map_val(v_type_expr)
        return super(BigMap, cls).empty(k_type_expr, v_type_expr)

    def __iter__(self):
        assert False, 'not supported'


class Timestamp(Int, prim='timestamp'):
    pass


class Mutez(Nat, prim='mutez'):
    pass


class Address(StackItem, prim='address'):
    pass


class Contract(StackItem, prim='contract'):
    pass


class Operation(StackItem, prim='operation'):
    pass


class Key(StackItem, prim='key'):
    pass


class KeyHash(String, prim='key_hash'):

    def __init__(self, value, val_expr=None, type_expr=None):
        assert is_pkh(value), f'expected key hash, got {value}'
        super(KeyHash, self).__init__(value, val_expr=val_expr, type_expr=type_expr)


class Signature(StackItem, prim='signature'):
    pass


class ChainID(StackItem, prim='chain_id'):
    pass


class Lambda(StackItem, prim='lambda', args_len=2):

    @classmethod
    def new(cls, p_type_expr, r_type_expr, code):
        return cls(
            val_expr={'prim': 'Lambda', 'args': [code]},
            type_expr={'prim': 'lambda', 'args': [p_type_expr, r_type_expr]})

    def assert_param_type(self, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(self.type_expr['args'][0], item.type_expr)

    def assert_ret_type(self, item: StackItem):
        assert_stack_item(item)
        assert_expr_equal(self.type_expr['args'][1], item.type_expr)

    # def apply(self, item: StackItem):
    #     p_type_expr = self.type_expr['args'][0]
    #     assert_prim(p_type_expr, prim='pair', args_len=2)
    #     left_type_expr = p_type_expr['args'][0]
    #     assert left_type_expr == item.type_expr, f'Expected {pformat(left_type_expr)}, got {pformat(item.type_expr)}'
    #     push = {'prim': 'PUSH', 'args': [item.type_expr, item.val_expr]}
