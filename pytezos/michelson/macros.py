import re
import functools

COMPARE = dict(prim='COMPARE')
UNIT = dict(prim='UNIT')
FAILWITH = dict(prim='FAILWITH')
DUP = dict(prim='DUP')
SWAP = dict(prim='SWAP')
CAR = dict(prim='CAR')
CDR = dict(prim='CDR')

primitives = {
    'ABS', 'ADD', 'ADDRESS', 'AMOUNT', 'AND', 'BALANCE', 'BLAKE2B', 'CAR', 'CAST',
    'CDR', 'CHECK_SIGNATURE', 'COMPARE', 'CONCAT', 'CONS', 'CONTRACT',
    'CREATE_ACCOUNT', 'CREATE_CONTRACT', 'DIP', 'DROP', 'DUP', 'EDIV', 'EMPTY_MAP',
    'EMPTY_SET', 'EQ', 'EXEC', 'Elt', 'FAILWITH', 'False', 'GE', 'GET', 'GT',
    'HASH_KEY', 'IF', 'IF_CONS', 'IF_LEFT', 'IF_NONE', 'IMPLICIT_ACCOUNT', 'INT',
    'ISNAT', 'ITER', 'LAMBDA', 'LE', 'LEFT', 'LOOP', 'LOOP_LEFT', 'LSL', 'LSR',
    'LT', 'Left', 'MAP', 'MEM', 'MUL', 'NEG', 'NEQ', 'NIL', 'NONE', 'NOT', 'NOW',
    'None', 'OR', 'PACK', 'PAIR', 'PUSH', 'Pair', 'RENAME', 'RIGHT', 'Right',
    'SELF', 'SENDER', 'SET_DELEGATE', 'SHA256', 'SHA512', 'SIZE', 'SLICE', 'SOME',
    'SOURCE', 'STEPS_TO_QUOTA', 'SUB', 'SWAP', 'Some', 'TRANSFER_TOKENS', 'True',
    'UNIT', 'UNPACK', 'UPDATE', 'Unit', 'XOR', 'address', 'big_map', 'bool',
    'bytes', 'code', 'contract', 'int', 'key_hash', 'key', 'lambda', 'list', 'map',
    'mutez', 'nat', 'operation', 'option', 'or', 'pair', 'parameter', 'set',
    'signature', 'storage', 'string', 'timestamp', 'unit'
}

__macros__ = []


def macro(regexp):
    def register_macro(func):
        __macros__.append((re.compile(regexp), func))
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return register_macro


def expand_macro(prim, annots, args):
    if prim in primitives:
        return make_dict(prim=prim, annots=annots, args=args)

    for regexp, handler in __macros__:
        groups = regexp.findall(prim)
        if groups:
            assert len(groups) == 1
            return handler(groups[0], annots, args)

    assert False, f'Unknown macro: {prim}'


def make_dict(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


@macro(r'CMP(EQ|NEQ|LT|GT|LE|GE)')
def expand_cmpx(prim, annots, args) -> list:
    assert not args
    return [
        COMPARE,
        make_dict(prim=prim[3:], annots=annots)
    ]


@macro(r'IF(EQ|NEQ|LT|GT|LE|GE)')
def expand_ifx(prim, annots, args) -> list:
    assert len(args) == 2
    return [
        make_dict(prim=prim, annots=annots),
        dict(prim='IF', args=args)
    ]


@macro(r'IFCMP(EQ|NEQ|LT|GT|LE|GE)')
def expand_ifcmpx(prim, annots, args) -> list:
    assert len(args) == 2
    return [
        COMPARE,
        make_dict(prim=prim, annots=annots),
        dict(prim='IF', args=args)
    ]


@macro(r'FAIL')
def expand_fail(prim, annots, args) -> list:
    assert not annots
    assert not args
    return [UNIT, FAILWITH]


@macro(r'ASSERT')
def expand_assert(prim, annots, args) -> dict:
    assert not annots
    assert not args
    return dict(prim='IF', args=[[], expand_fail()])


@macro(r'ASSERT_(EQ|NEQ|LT|LE|GT|GE)')
def expand_assertx(prim, annots, args) -> list:
    assert not args
    return expand_ifx(
        prim=prim,
        annots=annots,
        args=[[], expand_fail()]
    )


@macro(r'ASSERT_CMP(EQ|NEQ|LT|LE|GT|GE)')
def expand_assert_cmpx(prim, annots, args) -> list:
    assert not args
    return expand_ifcmpx(
        prim=prim,
        annots=annots,
        args=[[], expand_fail()]
    )


@macro(r'ASSERT_NONE')
def expand_assert_none(prim, annots, args) -> dict:
    assert not annots
    assert not args
    return dict(prim='IF_NONE', args=[[], expand_fail()])


@macro('ASSERT_SOME')
def expand_assert_x(prim, annots, args) -> dict:
    assert not args
    return dict(prim='IF_NONE', args=[
        expand_fail(),
        [make_dict(prim='RENAME', annots=annots)]
    ])


@macro('ASSERT_LEFT')
def expand_assert_left(prim, annots, args) -> dict:
    assert not args
    return dict(prim='IF_LEFT', args=[
        [make_dict(prim='RENAME', annots=annots)],
        expand_fail()
    ])


@macro('ASSERT_RIGHT')
def expand_assert_right(prim, annots, args) -> dict:
    assert not args
    return dict(prim='IF_LEFT', args=[
        expand_fail(),
        [make_dict(prim='RENAME', annots=annots)]
    ])


@macro(r'DII+P')
def expand_diip(prim, annots, args) -> dict:
    assert len(args) == 1
    assert not annots
    return dict(prim='DIP',
                args=[[expand_macro(prim=f'{prim[:-2]}P', annots=None, args=args)]])


@macro(r'DUU+P')
def expand_duup(prim, annots, args) -> list:
    assert not args
    return [dict(prim='DIP',
                 args=[expand_duup(prim=f'{prim[:-2]}P', annots=annots, args=None)]),
            SWAP]


def split_pair_annots(annots):
    if isinstance(annots, list):
        assert len(annots) >= 2, 'Not enough annotations for this macro'
        return annots[:2], annots[2:] if len(annots) > 2 else None
    else:
        return None, None


def expand_pair_macro(prim, annots, args):
    assert not args
    lr_annots, nested_annots = split_pair_annots(annots)
    pair = make_dict(prim='PAIR', annots=lr_annots)
    nested_pair = expand_macro(prim=f'{prim}R', annots=nested_annots, args=None)
    return pair, nested_pair if isinstance(nested_pair, list) else [nested_pair]


@macro(r'^PA([PAI]{2,})R$')
def expand_paxr(prim, annots, args) -> list:
    pair, nested_pair = expand_pair_macro(prim, annots, args)
    return [dict(prim='DIP', args=[nested_pair]), pair]


@macro(r'^P([PAI]{2,})IR$')
def expand_pxir(prim, annots, args) -> list:
    pair, nested_pair = expand_pair_macro(prim, annots, args)
    return [pair, *nested_pair]


@macro(r'UNPAIR')
def expand_unpair(prim, annots, args) -> list:
    assert not args
    if isinstance(annots, list):
        left, right = list(map(lambda x: [x], annots))
    else:
        left, right = None, None
    return [
        DUP,
        make_dict(prim='CAR', annots=left),
        dict(prim='DIP', args=[[make_dict(prim='CDR', annots=right)]])
    ]


def expand_unpair_macro(prim, annots, args):
    assert not args
    lr_annots, nested_annots = split_pair_annots(annots)
    unpair = expand_unpair(prim=None, annots=lr_annots, args=None)
    nested_unpair = expand_macro(prim=f'UN{prim}R', annots=nested_annots, args=None)
    return unpair, nested_unpair


@macro(r'^UNPA([PAI]{2,})R$')
def expand_unpaxr(prim, annots, args) -> list:
    unpair, nested_unpair = expand_unpair_macro(prim, annots, args)
    return [*unpair, dict(prim='DIP', args=[nested_unpair])]


@macro(r'^UNP([PAI]+)IR$')
def expand_unpxir(prim, annots, args) -> list:
    unpair, nested_unpair = expand_unpair_macro(prim, annots, args)
    return [*unpair, *nested_unpair]


def expand_cadr_macro(prim, annots, args) -> list:
    assert not args
    cadr = expand_macro(prim=f'C{prim}R', annots=annots, args=None)
    return cadr if isinstance(cadr, list) else [cadr]


@macro(r'^CA([AD]+)R$')
def expand_caxr(prim, annots, args) -> list:
    return [CAR, *expand_cadr_macro(prim, annots, args)]


@macro(r'^CD([AD]+)R$')
def expand_cdxr(prim, annots, args) -> list:
    return [CDR, *expand_cadr_macro(prim, annots, args)]


@macro(r'IF_SOME')
def expand_if_some(prim, annots, args) -> dict:
    assert not annots
    assert len(args) == 2
    return dict(prim='IF_NONE', args=args)


def split_cadr_annots(annots):
    if isinstance(annots, list):
        var_annots = list(filter(lambda x: x[0] == '@', annots))
        field_annots = list(filter(lambda x: x[0] == '%', annots))
        assert len(var_annots) <= 1, 'Too many variable annotations'
        assert len(field_annots) <= 1, 'Too many field annotations'
        return var_annots, field_annots
    else:
        return None, None


def expand_set_map_cadr_macro(prim, annots, args):
    var_annots, field_annots = split_cadr_annots(annots)
    cadr = make_dict(prim=prim, annots=field_annots)
    pair = make_dict(prim='PAIR', annots=var_annots)
    return cadr, pair


@macro(r'SET_(CAR|CDR)')
def expand_set(prim, annots, args) -> list:
    assert not args
    cadr, pair = expand_set_map_cadr_macro(prim, annots, args)
    return [cadr, SWAP, pair]


def expand_set_cadr_macro(prim, annots, args):
    assert not args
    var_annots, field_annots = split_cadr_annots(annots)
    cadr = expand_macro(prim=f'SET_C{prim}R', annots=field_annots, args=None)
    pair = make_dict(prim='PAIR', annots=var_annots)
    return cadr, pair


@macro(r'^SET_CA([AD]+)R$')
def expand_set_caxr(prim, annots, args) -> list:
    cadr, pair = expand_set_cadr_macro(prim, annots, args)
    return [DUP,
            dict(prim='DIP', args=[CAR, *cadr]),
            CDR,
            SWAP,
            pair]


@macro(r'^SET_CD([AD]+)R$')
def expand_set_cdxr(prim, annots, args) -> list:
    cadr, pair = expand_set_cadr_macro(prim, annots, args)
    return [DUP,
            dict(prim='DIP', args=[CDR, *cadr]),
            CAR,
            pair]


@macro(r'MAP_(CAR)')
def expand_map_car(prim, annots, args) -> list:
    car, pair = expand_set_map_cadr_macro(prim, annots, args)
    return [DUP,
            CDR,
            dict(prim='DIP', args=[[car, *args]]),
            SWAP,
            pair]


@macro(r'MAP_(CDR)')
def expand_map_cdr(prim, annots, args) -> list:
    cdr, pair = expand_set_map_cadr_macro(prim, annots, args)
    return [DUP,
            cdr,
            *args,
            SWAP,
            CAR,
            pair]


def expand_map_cadr_macro(prim, annots, args):
    var_annots, field_annots = split_cadr_annots(annots)
    cadr = expand_macro(prim=f'MAP_C{prim}R', annots=field_annots, args=args)
    pair = make_dict(prim='PAIR', annots=var_annots)
    return cadr, pair


@macro(r'^MAP_CA([AD]+)R$')
def expand_map_caxr(prim, annots, args) -> list:
    cadr, pair = expand_map_cadr_macro(prim, annots, args)
    return [DUP,
            dict(prim='DIP', args=[[CAR, *cadr]]),
            CDR,
            SWAP,
            pair]


@macro(r'^MAP_CD([AD]+)R$')
def expand_map_cdxr(prim, annots, args) -> list:
    cadr, pair = expand_map_cadr_macro(prim, annots, args)
    return [DUP,
            dict(prim='DIP', args=[[CDR, *cadr]]),
            CAR,
            pair]
