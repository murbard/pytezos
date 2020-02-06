from pytezos.michelson.converter import micheline_to_michelson


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
    if isinstance(res, callable):
        return res(args)
    else:
        return res


def parse_core_expr(expr) -> tuple:
    assert isinstance(expr, dict), f'expected dict, got {type(expr)}'
    assert len(expr.keys()) == 1, f'expected single key, got {len(expr.keys())}'
    core_type = next(iter(expr))
    return core_type, expr[core_type]


def get_core_val(val_expr, core_type):
    act_type, value = parse_core_expr(val_expr)
    assert core_type == act_type, f'expected {core_type}, got {act_type}'
    return value


def dispatch_core_map(val_expr, mapping: dict):
    act_type, val = parse_core_expr(val_expr)
    expected = ' or '.join(map(lambda x: f'`{x}`', mapping))
    assert act_type in mapping, f'expected {expected}, got {act_type}'
    res = mapping[act_type]
    if isinstance(res, callable):
        return res(val)
    else:
        return res


def assert_expr_equal(expected, actual):
    def equal(a, b):
        if type(a) != type(b):
            return False
        elif isinstance(a, dict):
            if a['prim'] != b['prim']:
                return False
            else:
                return equal(a.get('args', []), b.get('args', []))
        elif isinstance(a, list):
            if len(a) != len(b):
                return False
            else:
                return all(map(lambda i: equal(a[i], b[i]), range(len(a))))
        else:
            assert False, (a, b)
    assert equal(expected, actual), \
        f'expected {micheline_to_michelson(expected)}, got {micheline_to_michelson(actual)}'


def assert_comparable(type_expr) -> bool:
    pass


def assert_big_map_val(type_expr) -> bool:
    pass

#
# def assert_pushable(type_expr):
#     assert item.is_pushable(), f'{type(item).__name__} is not pushable'


def get_string(val_expr):
    return int(get_core_val(val_expr, core_type='string'))


def get_int(val_expr):
    return int(get_core_val(val_expr, core_type='int'))


def get_bytes(val_expr):
    return bytes.fromhex(get_core_val(val_expr, core_type='bytes'))
