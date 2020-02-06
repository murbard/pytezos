import functools
import calendar
from datetime import datetime
from typing import Tuple, Callable

from pytezos.michelson.converter import micheline_to_michelson
import pytezos.encoding as encoding

parsers = {}


def primitive(prim, args_len=0):
    def register_primitive(func):
        parsers[prim] = (args_len, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_primitive


def assert_list(val_expr):
    assert isinstance(val_expr, list), f'expected list, got {type(val_expr)}'


def parse_prim_expr(expr) -> tuple:
    assert isinstance(expr, dict), f'expected dict, got {type(expr)}'
    assert 'prim' in expr, f'primitive is absent'
    return expr['prim'], expr.get('args', [])


def get_prim_args(val_expr, prim, args_len: int):
    p, args = parse_prim_expr(val_expr)
    assert p == prim, f'expected {prim}, got {p}'
    assert len(args) == args_len, f'expected {args_len} args, got {len(args)}'
    return args


def dispatch_prim_map(val_expr, mapping: dict):
    p, args = parse_prim_expr(val_expr)
    expected = ' or '.join(map(lambda x: f'{x[0]} ({x[1]} args)', mapping))
    assert (p, len(args)) in mapping, f'expected {expected}, got {p} ({len(args)} args)'
    res = mapping[(p, len(args))]
    if callable(res):
        return res(args)
    else:
        return res


def parse_core_expr(expr) -> tuple:
    assert isinstance(expr, dict), f'expected dict, got {type(expr)}'
    assert len(expr.keys()) == 1, f'expected single key, got {len(expr.keys())}'
    core_type = next(iter(expr))
    return core_type, expr[core_type]


def dispatch_core_map(val_expr, mapping: dict):
    act_type, val = parse_core_expr(val_expr)
    expected = ' or '.join(map(lambda x: f'`{x}`', mapping))
    assert act_type in mapping, f'expected {expected}, got {act_type}'
    res = mapping[act_type]
    if callable(res):
        return res(val)
    else:
        return res


def get_core_val(val_expr, core_type):
    act_type, value = parse_core_expr(val_expr)
    assert core_type == act_type, f'expected {core_type}, got {act_type}'
    return value


def get_string(val_expr):
    return int(get_core_val(val_expr, core_type='string'))


def get_int(val_expr):
    return int(get_core_val(val_expr, core_type='int'))


def get_bytes(val_expr):
    return bytes.fromhex(get_core_val(val_expr, core_type='bytes'))


def expr_equal(a, b):
    if type(a) != type(b):
        return False
    elif isinstance(a, dict):
        if a.get('prim'):
            if a['prim'] != b['prim']:
                return False
            else:
                return expr_equal(a.get('args', []), b.get('args', []))
        else:
            return a == b
    elif isinstance(a, list):
        if len(a) != len(b):
            return False
        else:
            return all(map(lambda i: expr_equal(a[i], b[i]), range(len(a))))
    else:
        assert False, (a, b)


def assert_expr_equal(expected, actual):
    assert expr_equal(expected, actual), \
        f'expected {micheline_to_michelson(expected)}, got {micheline_to_michelson(actual)}'


def is_comparable(type_expr):
    prim, args, _ = parse_type(type_expr)
    comparable_types = {
        'string', 'int', 'bytes', 'nat', 'bool'
        'address', 'key_hash', 'mutez', 'timestamp'
    }
    if prim in comparable_types:
        return True
    elif prim == 'pair':
        left, _ = parse_prim_expr(args[0])
        return left != 'pair' and all(map(is_comparable, args))
    else:
        return False


def assert_comparable(type_expr):
    assert is_comparable(type_expr), f'type is not comparable: {micheline_to_michelson(type_expr)}'


def assert_pushable(type_expr):
    pass


def is_big_map_val(type_expr):
    prim, args, _ = parse_type(type_expr)
    if prim in ['big_map', 'operation']:
        return False
    return all(map(is_big_map_val, args))


def assert_big_map_val(type_expr):
    assert is_big_map_val(type_expr), f'cannot be a big map value: {micheline_to_michelson(type_expr)}'


def parse_type(type_expr) -> Tuple[str, list, Callable]:
    prim, args = parse_prim_expr(type_expr)
    assert prim in parsers, f'{prim}: unknown primitive '
    args_len, func = parsers[prim]
    assert len(args) == args_len, f'{prim}: expected {args_len} arg(s), got {len(args)}'
    return prim, args, func


def parse_value(val_expr, type_expr):
    _, args, func = parse_type(type_expr)
    return func(val_expr, args)


@primitive('string')
def parse_string(val_expr, type_args):
    return get_string(val_expr)


@primitive('int')
def parse_int(val_expr, type_args):
    return get_int(val_expr)


@primitive('bytes')
def parse_bytes(val_expr, type_args):
    return get_bytes(val_expr)


@primitive('nat')
def parse_nat(val_expr, type_args):
    value = get_int(val_expr)
    assert value >= 0, f'nat cannot be negative ({value})'
    return value


@primitive('bool')
def parse_bool(val_expr, type_args):
    return dispatch_prim_map(val_expr, {
        ('False', 0): False,
        ('True', 0): True
    })


@primitive('unit')
def parse_unit(val_expr, type_args):
    _ = get_prim_args(val_expr, prim='Unit', args_len=0)


@primitive('list', args_len=1)
def parse_list(val_expr, type_args):
    assert_list(val_expr)
    return [parse_value(item, type_args[0]) for item in val_expr]


@primitive('pair', args_len=2)
def parse_pair(val_expr, type_args):
    args = get_prim_args(val_expr, prim='Pair', args_len=2)
    return tuple(parse_value(args[i], type_args[i]) for i in [0, 1])


@primitive('option', args_len=1)
def parse_option(val_expr, type_args):
    return dispatch_prim_map(val_expr, {
        ('None', 0): None,
        ('Some', 1): lambda x: parse_value(x[0], type_args[0])
    })


@primitive('or', args_len=2)
def parse_or(val_expr, type_args):
    return dispatch_prim_map(val_expr, {
        ('Left', 1): lambda x: parse_value(x[0], type_args[0]),
        ('Right', 1): lambda x: parse_value(x[0], type_args[1])
    })


@primitive('set', args_len=1)
def parse_set(val_expr, type_args):
    assert_list(val_expr)
    assert_comparable(type_args[0])
    value = {parse_value(item, type_args[0]) for item in val_expr}
    assert len(value) == len(val_expr), f'found duplicate elements'
    return value


def parse_elt(val_expr, type_args) -> tuple:
    k_val_expr, v_val_expr = get_prim_args(val_expr, prim='Elt', args_len=2)
    return parse_value(k_val_expr, type_args[0]), parse_value(v_val_expr, type_args[1])


@primitive('map', args_len=2)
def parse_map(val_expr, type_args):
    assert_list(val_expr)
    assert_comparable(type_args[0])
    return dict(parse_elt(item, type_args) for item in val_expr)


@primitive('big_map', args_len=2)
def parse_big_map(val_expr, type_args):
    assert_big_map_val(type_args[1])
    return parse_map(val_expr, type_args)


def strptime(s) -> int:
    dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    return calendar.timegm(dt.utctimetuple())


@primitive('timestamp')
def parse_timestamp(val_expr, type_args):
    return dispatch_core_map(val_expr, {'int': int, 'string': strptime})


@primitive('mutez')
def parse_mutez(val_expr, type_args):
    return parse_nat(val_expr, type_args)


@primitive('address')
def parse_address(val_expr, type_args):
    return dispatch_core_map(val_expr, {
        'bytes': lambda x: encoding.parse_address(bytes.fromhex(x)),
        'string': lambda x: x
    })


@primitive('contract', args_len=1)
def parse_contract(val_expr, type_args):  # TODO: entrypoint?
    return parse_address(val_expr, type_args)


@primitive('operation')
def parse_operation(val_expr, type_args):
    assert False, 'cannot parse an operation'


@primitive('key')
def parse_key(val_expr, type_args):
    return dispatch_core_map(val_expr, {
        'bytes': lambda x: encoding.parse_public_key(bytes.fromhex(x)),
        'string': lambda x: x
    })


@primitive('key_hash')
def parse_key_hash(val_expr, type_args):
    return parse_address(val_expr, type_args)


@primitive('signature')
def parse_signature(val_expr, type_args):
    return get_string(val_expr)


@primitive('chain_id')
def parse_chain_id(val_expr, type_args):
    return get_string(val_expr)


@primitive('lambda', args_len=2)
def parse_lambda(val_expr, type_args):
    code, = get_prim_args(val_expr, 'Lambda', args_len=1)
    return code
