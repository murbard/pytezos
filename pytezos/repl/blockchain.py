from datetime import datetime

from pytezos import pytezos
from pytezos.repl.control import instruction
from pytezos.repl.context import Context
from pytezos.repl.types import assert_stack_type, Mutez, ChainID, Address, Contract, Option, assert_equal_types, \
    KeyHash, Timestamp, expr_equal
from pytezos.repl.parser import get_entry_expr

MAINNET_CHAIN_ID = 'NetXdQprcVkpaWU'
UNIT_TYPE_EXPR = {'prim': 'unit'}
SELF_ADDRESS = 'KT1VG2WtYdSWz5E7chTeAdDPZNy2MpP8pTfL'


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


@instruction('AMOUNT')
def do_amount(ctx: Context, prim, args, annots):
    res = ctx.get('AMOUNT', Mutez(0))
    ctx.push(res, annots=annots)


@instruction('BALANCE')
def do_balance(ctx: Context, prim, args, annots):
    res = ctx.get('BALANCE', Mutez(0))
    ctx.push(res, annots=annots)


@instruction('CHAIN_ID')
def do_chain_id(ctx: Context, prim, args, annots):
    res = ctx.get('CHAIN_ID', ChainID(MAINNET_CHAIN_ID))
    ctx.push(res, annots=annots)


@instruction('SELF')
def do_self(ctx: Context, prim, args, annots):
    p_type_expr = ctx.get('parameter')
    assert p_type_expr, f'parameter type is not initialized'

    entrypoint = next((a for a in annots if a[0] == '%'), '%default')
    ctx.printf(f' use {entrypoint};')

    p_type_expr = get_entry_expr(p_type_expr, entrypoint)
    res = Contract.new(SELF_ADDRESS + entrypoint, type_expr=p_type_expr)
    ctx.push(res, annots=[a for a in annots if a[0] != '%'])


@instruction('SENDER')
def do_sender(ctx: Context, prim, args, annots):
    res = ctx.get('SENDER')
    assert res, f'SENDER is not initialized'
    ctx.push(res, annots=annots)


@instruction('SOURCE')
def do_source(ctx: Context, prim, args, annots):
    res = ctx.get('SOURCE')
    assert res, f'SOURCE is not initialized'
    ctx.push(res, annots=annots)


@instruction('NOW')
def do_now(ctx: Context, prim, args, annots):
    res = ctx.get('NOW')
    if not res:
        chain_id = ctx.get('CHAIN_ID')
        if chain_id:
            now = pytezos.using(get_network_by_chain_id(chain_id)).now()
        else:
            now = int(datetime.utcnow().timestamp())
        res = Timestamp(now)
    ctx.push(res, annots=annots)


def check_contract(ctx: Context, address, type_expr):
    chain_id = ctx.get('CHAIN_ID')
    if not chain_id:
        ctx.printf(' skip check;')
        return True

    network = get_network_by_chain_id(chain_id)

    try:
        ci = pytezos.using(network).contract(address)
        if expr_equal(type_expr, ci.contract.parameter.code):
            return True
        else:
            ctx.printf(' type mismatch;')
    except Exception:
        ctx.printf(' not found;')

    return False


@instruction('ADDRESS')
def do_address(ctx: Context, prim, args, annots):
    top = ctx.pop1()
    assert_stack_type(top, Contract)
    res = Address.new(str(top)[:36])
    ctx.push(res, annots=annots)


@instruction('CONTRACT', args_len=1)
def do_contract(ctx: Context, prim, args, annots):
    top = ctx.pop1()
    assert_stack_type(top, Address)
    contract = Contract.new(str(top), type_expr=args[0])
    if check_contract(ctx, address=str(top), type_expr=args[0]):
        res = Option.some(contract)
    else:
        res = Option.none(contract.type_expr)
    ctx.push(res, annots=annots)


@instruction('IMPLICIT_ACCOUNT')
def do_implicit_account(ctx: Context, prim, args, annots):
    top = ctx.pop1()
    assert_stack_type(top, KeyHash)
    res = Contract.new(str(top), type_expr=UNIT_TYPE_EXPR)
    ctx.push(res, annots=annots)


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
