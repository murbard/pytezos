import calendar
from pprint import pformat
from datetime import datetime

import pytezos.encoding as encoding

COMPARABLE = 1
PASSABLE = 2
STORABLE = 4
PUSHABLE = 8
PACKABLE = 16


def assert_list(node):
    assert isinstance(node, list), f'Expected list, got {type(node)}: {pformat(node)}'


def assert_dict(node):
    assert isinstance(node, dict), f'Expected dict, got {type(node)}: {pformat(node)}'


def assert_args_len(node, args_len: int):
    node_args = node.get('args', [])
    node_args_len = len(node_args)
    assert node_args_len == args_len, f'Expected {args_len} arg(s), got {node_args_len}: {pformat(node)}'


def check_prim(val_node, prim, args_len: int) -> bool:
    assert_dict(val_node)
    return val_node.get('prim') == prim \
        and len(val_node.get('args', [])) == args_len


def assert_prim(val_node, prim, args_len: int):
    assert check_prim(val_node, prim, args_len), f'Expected {prim} ({args_len} args): {pformat(val_node)}'


def check_type(val_node, core_type) -> bool:
    assert_dict(val_node)
    assert len(val_node.keys()) == 1, f'Expected single key, got {val_node.keys()}: {pformat(val_node)}'
    return next(iter(val_node)) == core_type


def assert_type(val_node, core_type):
    assert check_type(val_node, core_type), f'Expected {core_type}: {pformat(val_node)}'


class StackItem:
    flags = 0
    __cls__ = {}
    __prim__ = {}

    def __init__(self, type_node, val_node):
        self.type_node = type_node
        self.val_node = val_node
        self.value = object()

    @classmethod
    def __init_subclass__(cls, prim='', args_len=0, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__cls__[prim] = cls, args_len
        cls.__prim__[type(cls)] = prim

    def __cmp__(self, other):
        assert self.is_comparable(), f'Not a comparable type: {type(self)}'
        assert type(self) == type(other), f'Different types: {type(self)} vs {type(other)}'
        if self.value < other.value:
            res = -1
        elif self.value > other.value:
            res = 1
        else:
            res = 0
        return Int.new(res)

    def __abs__(self):
        assert False, 'Not allowed'

    def __add__(self, other):
        assert False, 'Not allowed'

    @classmethod
    def parse_type(cls, type_node):
        assert_dict(type_node)
        prim = type_node.get('prim')
        assert prim in StackItem.__cls__, f'Unknown primitive {prim}: {pformat(type_node)}'
        item_class, args_len = StackItem.__cls__[type_node['prim']]
        assert_args_len(type_node, args_len)
        return item_class

    @classmethod
    def parse(cls, type_node, val_node):
        item_class = cls.parse_type(type_node)
        return item_class(type_node=type_node, val_node=val_node)

    @classmethod
    def new(cls, value):
        prim = cls.__prim__[type(cls)]
        if isinstance(value, str):
            core_type = 'string'
        elif isinstance(value, int):
            core_type = 'int'
            value = str(value)
        elif isinstance(value, bytes):
            core_type = 'bytes'
            value = value.hex()
        else:
            assert False, f'Unexpected core type: {type(value)}'
        return cls(type_node={'prim': prim}, val_node={core_type: value})

    def is_comparable(self) -> bool:
        return self.flags & COMPARABLE != 0

    def contains_big_map(self) -> bool:
        child_cls = [StackItem.parse_type(arg) for arg in self.type_node['args']]
        return any(map(lambda x: type(x) == BigMap or x.contains_big_map(), child_cls))


class String(StackItem, prim='string'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, type_node, val_node):
        super(String, self).__init__(type_node, val_node)
        assert_type(val_node, core_type='string')
        self.value = val_node['string']


class Int(StackItem, prim='int'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, type_node, val_node):
        super(Int, self).__init__(type_node, val_node)
        assert_type(val_node, core_type='int')
        self.value = int(val_node['int'])

    def __abs__(self):
        return Nat.new(abs(self.value))

    def __add__(self, other):
        if type(other) in [Int, Nat]:
            return Int.new(self.value + other.value)
        elif type(other) == Timestamp:
            return Timestamp.new(self.value + other.value)
        else:
            assert False, f'Unexpected operand type: {type(other)}'

    def __divmod__(self, other):
        if type(other) in [Int, Nat]:
            if other.value == 0:
                return Option.none(Pair.make(Int.new(0), Int.new(0)))
            else:
                q, r = divmod(self.value, other.value)
                if r < 0:
                    r += abs(other.value)
                    q += 1
                return Option.some(Pair.make(Int.new(q), Int.new(r)))


class Bytes(StackItem, prim='bytes'):
    flags = COMPARABLE | PASSABLE | STORABLE | PUSHABLE | PACKABLE

    def __init__(self, type_node, val_node):
        super(Bytes, self).__init__(type_node, val_node)
        assert_type(val_node, core_type='bytes')
        self.value = bytes.fromhex(val_node['bytes'])


class Nat(Int, prim='nat'):

    def __init__(self, type_node, val_node):
        super(Nat, self).__init__(type_node, val_node)
        assert self.value >= 0, f'Cannot be negative: {self.value}'

    def __abs__(self):
        assert False, 'Not allowed'

    def __add__(self, other):
        if type(other) == Int:
            return Int.new(self.value + other.value)
        elif type(other) == Nat:
            return Nat.new(self.value + other.value)
        else:
            assert False, f'Unexpected operand type: {type(other)}'


class Bool(StackItem, prim='bool'):

    def __init__(self, type_node, val_node):
        super(Bool, self).__init__(type_node, val_node)
        if check_prim(val_node, prim='False', args_len=0):
            self.value = False
        elif check_prim(val_node, prim='True', args_len=0):
            self.value = True
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'


class Unit(StackItem, prim='unit'):

    def __init__(self, type_node, val_node):
        super(Unit, self).__init__(type_node, val_node)
        assert_prim(val_node, prim='Unit', args_len=0)


class List(StackItem, prim='list', args_len=1):

    def __init__(self, type_node, val_node):
        super(List, self).__init__(type_node, val_node)
        assert_list(val_node)
        elt_cls = StackItem.parse_type(type_node['args'][0])
        self.value = [elt_cls(type_node['args'][0], item) for item in val_node]


class Pair(StackItem, prim='pair', args_len=1):

    def __init__(self, type_node, val_node):
        super(Pair, self).__init__(type_node, val_node)
        assert_prim(val_node, prim='Pair', args_len=2)
        self.value = tuple(StackItem.parse(type_node['args'][i], val_node['args'][i]) for i in [0, 1])

    def is_comparable(self):
        left_cls, right_cls = [StackItem.parse_type(arg) for arg in self.type_node['args']]
        return type(left_cls) != Pair and right_cls.is_comparable()

    @classmethod
    def make(cls, left: StackItem, right: StackItem):
        return Pair(type_node={'prim': 'pair', 'args': [left.type_node, right.type_node]},
                    val_node={'prim': 'Pair', 'args': [left.val_node, right.val_node]})


class Option(StackItem, prim='pair', args_len=1):

    def __init__(self, type_node, val_node):
        super(Option, self).__init__(type_node, val_node)
        if check_prim(val_node, prim='None', args_len=0):
            self.value = None
        elif check_prim(val_node, prim='Some', args_len=1):
            self.value = StackItem.parse(type_node['args'][0], val_node['args'][0])
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'

    @classmethod
    def none(cls, item: StackItem):
        return Option(type_node={'prim': 'option', 'args': [item.type_node]},
                      val_node={'prim': 'None'})

    @classmethod
    def some(cls, item: StackItem):
        return Option(type_node={'prim': 'option', 'args': [item.type_node]},
                      val_node={'prim': 'Some', 'args': [item.val_node]})


class Or(StackItem, prim='or', args_len=2):

    def __init__(self, type_node, val_node):
        super(Or, self).__init__(type_node, val_node)
        if check_prim(val_node, prim='Left', args_len=1):
            idx = 0
        elif check_prim(val_node, prim='Right', args_len=1):
            idx = 1
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'

        self.value = StackItem.parse(type_node['args'][idx], val_node['args'][0])


class Set(StackItem, prim='set', args_len=1):

    def __init__(self, type_node, val_node):
        super(Set, self).__init__(type_node, val_node)
        assert_list(val_node)
        elt_cls = StackItem.parse_type(type_node['args'][0])
        assert elt_cls.is_comparable(), f'Expected comparable item type: {pformat(type_node)}'

        self.value = {elt_cls(type_node['args'][0], item) for item in val_node}
        assert len(self.value) == len(val_node), f'Duplicate elements found: {pformat(val_node)}'


class Map(StackItem, prim='map', args_len=1):

    def __init__(self, type_node, val_node):
        super(Map, self).__init__(type_node, val_node)
        assert_list(val_node)
        key_cls, val_cls = [StackItem.parse_type(arg) for arg in type_node['args']]
        assert key_cls.is_comparable(), f'Expected comparable key type: {pformat(type_node)}'

        def parse_elt(elt):
            assert_prim(elt, prim='Elt', args_len=2)
            return key_cls(type_node['args'][0], elt['args'][0]), \
                   val_cls(type_node['args'][1], elt['args'][1])

        self.value = dict(map(parse_elt, val_node))
        assert len(self.value) == len(val_node), f'Duplicate keys found: {pformat(val_node)}'


class BigMap(Map, prim='big_map', args_len=1):

    def __init__(self, type_node, val_node):
        super(BigMap, self).__init__(type_node, val_node)
        assert not self.contains_big_map(), f'Big map cannot contain big maps: {pformat(type_node)}'


class Timestamp(StackItem, prim='timestamp'):

    def __init__(self, type_node, val_node):
        super(Timestamp, self).__init__(type_node, val_node)
        if check_type(val_node, 'int'):
            self.value = int(val_node['int'])
        elif check_type(val_node, 'string'):
            dt = datetime.strptime(val_node['string'], '%Y-%m-%dT%H:%M:%SZ')
            self.value = calendar.timegm(dt.utctimetuple())
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'

    def __add__(self, other):
        assert type(other) == Int, f'Unexpected operand type: {type(other)}'
        return Timestamp.new(self.value + other.value)


class Mutez(Nat, prim='mutez'):

    def __add__(self, other):
        assert type(other) == Mutez, f'Unexpected operand type: {type(other)}'
        return Mutez.new(self.value + other.value)


class Address(StackItem, prim='address'):

    def __init__(self, type_node, val_node):
        super(Address, self).__init__(type_node, val_node)
        if check_type(val_node, core_type='string'):
            self.value = val_node['string']
        elif check_type(val_node, core_type='bytes'):
            data = bytes.fromhex(val_node['bytes'])
            self.value = encoding.parse_address(data)
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'


class Contract(Address, prim='contract'):
    pass


class Operation(StackItem, prim='operation'):
    pass


class Key(StackItem, prim='key'):

    def __init__(self, type_node, val_node):
        super(Key, self).__init__(type_node, val_node)
        if check_type(val_node, core_type='string'):
            self.value = val_node['string']
        elif check_type(val_node, core_type='bytes'):
            data = bytes.fromhex(val_node['bytes'])
            self.value = encoding.parse_public_key(data)
        else:
            assert False, f'Expected {pformat(type_node)}: {pformat(val_node)}'


class KeyHash(Address, prim='key_hash'):
    pass


class Signature(StackItem, prim='signature'):
    pass


class ChainID(StackItem, prim='chain_id'):
    pass


class Lambda(StackItem, prim='lambda'):
    pass
