import functools
from pprint import pformat
from typing import Tuple, Callable
from decimal import Decimal

import pytezos.encoding as encoding

types = {}


class Unit(object):

    def __repr__(self):
        return 'Unit'


def primitive(prim, args_len=0):
    def register_type(func):
        types[prim] = (args_len, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_type


def is_comparable(type_node, pair_left_child=False):
    prim, args, _ = parse_type(type_node)
    comparable = {
        'string', 'int', 'bytes', 'nat', 'bool'
        'address', 'key_hash', 'mutez', 'timestamp'
    }
    if prim in comparable:
        return True
    if prim == 'pair' and not pair_left_child:
        return all(map(is_comparable, args))
    return False


def assert_comparable(type_node):
    assert is_comparable(type_node), f'Type is not comparable: {pformat(type_node)}'


def assert_types_equal(type_node1, type_node2):
    assert type_node1 == type_node2, f'Mismatched types: {pformat(type_node1)} vs {pformat(type_node2)}'


def has_big_map(type_node):
    prim, args, _ = parse_type(type_node)
    if prim == 'big_map':
        return True
    return any(map(has_big_map, args))


def assert_list(node):
    assert isinstance(node, list), f'Expected list, got {type(node)}: {pformat(node)}'


def assert_dict(node):
    assert isinstance(node, dict), f'Expected dict, got {type(node)}: {pformat(node)}'


def assert_prim(node, prim):
    node_prim = node.get('prim')
    assert node_prim == prim, f'Expected {prim} got {node_prim}: {pformat(node)}'


def assert_args_len(node, args_len: int):
    node_args = node.get('args', [])
    node_args_len = len(node_args)
    assert node_args_len == args_len, f'Expected {args_len} arg(s), got {node_args_len}: {pformat(node)}'


def parse_type(type_node) -> Tuple[str, list, Callable]:
    assert_dict(type_node)
    prim = type_node.get('prim')
    assert prim in types, f'Unknown primitive {prim}: {pformat(type_node)}'
    args = type_node.get('args', [])
    args_len, func = types[type_node['prim']]
    assert_args_len(type_node, args_len)
    return prim, args, func


def get_args(node, prim, args_len: int) -> list:
    assert_dict(node)
    assert_prim(node, prim)
    assert_args_len(node, args_len)
    return node['args']


def get_core_type(node) -> str:
    assert_dict(node)
    assert len(node.keys()) == 1, f'Expected single key, got {node.keys()}: {pformat(node)}'
    return next(iter(node))


def get_value(node, core_type) -> str:
    assert_dict(node)
    node_core_type = get_core_type(node)
    assert node_core_type == core_type, f'Expected {core_type}, got {node_core_type}: {pformat(node)}'
    return node[core_type]


def parse_expr(val_node, type_node):
    _, args, func = parse_type(type_node)
    return func(val_node, args)


@primitive('string')
def parse_string(val_node, type_args=None):
    return get_value(val_node, core_type='string')


@primitive('int')
def parse_int(val_node, type_args=None):
    value = get_value(val_node, core_type='int')
    return int(value)


@primitive('bytes')
def parse_bytes(val_node, type_args=None):
    value = get_value(val_node, core_type='bytes')
    return bytes.fromhex(value)


@primitive('nat')
def parse_nat(val_node, type_args):
    value = parse_int(val_node, type_args)
    assert value >= 0, f'Cannot be negative: {value}'
    return value


@primitive('bool')
def parse_bool(val_node, type_args):
    assert_dict(val_node)
    assert_args_len(val_node, 0)
    if val_node.get('prim') == 'False':
        return False
    else:
        assert_prim(val_node, 'True')
        return True


@primitive('unit')
def parse_unit(val_node, type_args=None):
    _ = get_args(val_node, prim='Unit', args_len=0)
    return Unit()


@primitive('list', args_len=1)
def parse_list(val_node, type_args):
    assert_list(val_node)
    return [parse_expr(item, type_args[0]) for item in val_node]


@primitive('pair', args_len=2)
def parse_pair(val_node, type_args):
    args = get_args(val_node, prim='Pair', args_len=2)
    return tuple(parse_expr(args[i], type_args[i]) for i in [0, 1])


@primitive('option', args_len=1)
def parse_option(val_node, type_args):
    assert_dict(val_node)
    if val_node.get('prim') == 'None':
        assert_args_len(val_node, 0)
        return None
    else:
        args = get_args(val_node, prim='Some', args_len=1)
        return parse_expr(args[0], type_args[0])


@primitive('or', args_len=2)
def parse_or(val_node, type_args):
    assert_dict(val_node)
    if val_node.get('prim') == 'Left':
        args = get_args(val_node, prim='Left', args_len=1)
        idx = 0
    else:
        args = get_args(val_node, prim='Right', args_len=1)
        idx = 1
    return parse_expr(args[0], type_args[idx])


@primitive('set', args_len=1)
def parse_set(val_node, type_args):
    assert_list(val_node)
    assert_comparable(type_args[0])
    assert len(set(val_node)) == len(val_node), f'Found duplicate elements: {pformat(val_node)}'
    return {parse_expr(item, type_args[0]) for item in val_node}


def parse_elt(val_node, type_args) -> tuple:
    k_node, v_node = get_args(val_node, prim='Elt', args_len=2)
    return parse_expr(k_node, type_args[0]), parse_expr(v_node, type_args[1])


@primitive('map', args_len=2)
def parse_map(val_node, type_args):
    assert_list(val_node)
    assert_comparable(type_args[0])
    return dict([parse_elt(item, type_args) for item in val_node])


@primitive('big_map', args_len=2)
def parse_big_map(val_node, type_args):
    assert not has_big_map(type_args[1]), f'Big map cannot contain big map: {pformat(type_args[1])}'
    return parse_map(val_node, type_args)


@primitive('timestamp')
def parse_timestamp(val_node, type_args=None):
    core_type = get_core_type(val_node)
    if core_type == 'int':
        pass  # TODO
    else:
        return get_value(val_node, 'string')


@primitive('mutez')
def parse_mutez(val_node, type_args):
    value = parse_nat(val_node, type_args)
    return Decimal(value) / 10 ** 6


@primitive('address')
def parse_address(val_node, type_args=None):
    core_type = get_core_type(val_node)
    if core_type == 'bytes':
        data = bytes.fromhex(val_node['bytes'])
        return encoding.parse_address(data)
    else:
        return get_value(val_node, 'string')


@primitive('contract', args_len=1)
def parse_contract(val_node, type_args):  # TODO: entrypoint
    return parse_address(val_node, type_args)


@primitive('operation')
def parse_operation(val_node, type_args):
    assert False, 'You should not be here'


@primitive('key')
def parse_key(val_node, type_args=None):
    core_type = get_core_type(val_node)
    if core_type == 'bytes':
        data = bytes.fromhex(val_node['bytes'])
        return encoding.parse_public_key(data)
    else:
        return get_value(val_node, 'string')


@primitive('key_hash')
def parse_key_hash(val_node, type_args):
    return parse_address(val_node, type_args)


@primitive('signature')
def parse_signature(val_node, type_args=None):
    return get_value(val_node, 'string')


@primitive('chain_id')
def parse_chain_id(val_node, type_args=None):
    return get_value(val_node, 'string')


@primitive('lambda', args_len=2)
def parse_lambda(val_node, type_args=None):
    args = get_args(val_node, 'Lambda', args_len=1)
    return args[0]
