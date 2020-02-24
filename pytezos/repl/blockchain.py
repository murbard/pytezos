from datetime import datetime

from pytezos import pytezos
from pytezos.repl.control import instruction
from pytezos.repl.context import Context
from pytezos.repl.types import assert_stack_type, Mutez, ChainID, Address, Contract, Option, assert_equal_types, \
    KeyHash, Timestamp
from pytezos.repl.parser import MichelsonTypeCheckError

MAINNET_CHAIN_ID = 'NetXdQprcVkpaWU'
UNIT_TYPE_EXPR = {'prim': 'unit'}


def get_network_by_chain_id(chain_id: ChainID):
    networks = {
        MAINNET_CHAIN_ID: 'mainnet'
    }
    key = str(chain_id)
    assert key in networks, f'unknown chain_id {key}'
    return networks[key]


@instruction('parameter', args_len=1)
def do_parameter(ctx: Context, prim, args, annots):
    ctx.set('parameter', args[0])


@instruction('storage', args_len=1)
def do_parameter(ctx: Context, prim, args, annots):
    ctx.set('storage', args[0])


@instruction('code', args_len=1)
def do_parameter(ctx: Context, prim, args, annots):
    ctx.set('code', args[0])


@instruction('ADDRESS')
def do_address(ctx: Context, prim, args, annots):
    res = ctx.get('ADDRESS')
    assert res, f'ADDRESS is not initialized'
    ctx.ins(res, annots=annots)


@instruction('AMOUNT')
def do_amount(ctx: Context, prim, args, annots):
    res = ctx.get('AMOUNT', Mutez(0))
    ctx.ins(res, annots=annots)


@instruction('BALANCE')
def do_balance(ctx: Context, prim, args, annots):
    res = ctx.get('BALANCE', Mutez(0))
    ctx.ins(res, annots=annots)


@instruction('CHAIN_ID')
def do_chain_id(ctx: Context, prim, args, annots):
    res = ctx.get('CHAIN_ID', ChainID(MAINNET_CHAIN_ID))
    ctx.ins(res, annots=annots)


@instruction('SELF')
def do_self(ctx: Context, prim, args, annots):
    p_type_expr = ctx.get('parameter')
    assert p_type_expr, f'parameter type is not initialized'
    address = ctx.get('ADDRESS')
    assert address, f'ADDRESS is not initialized'
    res = Contract.new(str(address), type_expr=p_type_expr)
    ctx.ins(res, annots=annots)


@instruction('SENDER')
def do_sender(ctx: Context, prim, args, annots):
    res = ctx.get('SENDER')
    assert res, f'SENDER is not initialized'
    ctx.ins(res, annots=annots)


@instruction('SOURCE')
def do_source(ctx: Context, prim, args, annots):
    res = ctx.get('SOURCE')
    assert res, f'SOURCE is not initialized'
    ctx.ins(res, annots=annots)


@instruction('NOW')
def do_now(ctx: Context, prim, args, annots):
    chain_id = ctx.get('CHAIN_ID')
    if chain_id:
        now = pytezos.using(get_network_by_chain_id(chain_id)).now()
    else:
        now = int(datetime.utcnow().timestamp())

    res = Timestamp(now)
    ctx.ins(res, annots=annots)


def assert_contract(chain_id, address, type_expr):
    network = get_network_by_chain_id(chain_id)
    try:
        ci = pytezos.using(network).contract(address)
    except Exception as e:
        raise MichelsonTypeCheckError(f'contract {address} is not found in the {network}', [])
    assert_equal_types(type_expr, ci.contract.parameter.code)


@instruction('CONTRACT', args_len=1)
def do_contract(ctx: Context, prim, args, annots):
    top = ctx.pop()
    assert_stack_type(top, Address)
    chain_id = ctx.get('CHAIN_ID')
    if chain_id:
        assert_contract(chain_id, address=str(top), type_expr=args[0])
    res = Contract.new(str(top), type_expr=args[0])
    ctx.ins(res, annots=annots)


@instruction('IMPLICIT_ACCOUNT')
def do_implicit_account(ctx: Context, prim, args, annots):
    top = ctx.pop()
    assert_stack_type(top, KeyHash)
    chain_id = ctx.get('CHAIN_ID')
    if chain_id:
        assert_contract(chain_id, address=str(top), type_expr=UNIT_TYPE_EXPR)
    res = Contract.new(str(top), type_expr=UNIT_TYPE_EXPR)
    ctx.ins(res, annots=annots)


@instruction('CREATE_CONTRACT', args_len=3)
def do_create_contract(ctx: Context, prim, args, annots):
    delegate, amount, storage = ctx.pop3()
    assert_stack_type(delegate, Option)
    assert_stack_type(amount, Mutez)
    assert_equal_types(args[0], storage.type_expr)

    internal_operation = {
        'script': {
            'code': args[2],
            'storage': storage.val_expr},
        'balance': int(amount),
        'delegate': str(next(iter(delegate))) if not delegate.is_none() else ''}
    # TODO:


@instruction('SET_DELEGATE')
def do_set_delegate(ctx: Context, prim, args, annots):
    pass  # TODO


@instruction('TRANSFER_TOKENS')
def do_transfer_tokens(ctx: Context, prim, args, annots):
    pass  # TODO
