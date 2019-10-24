import json
from os.path import join, dirname, exists
from os import mkdir

from pytezos import pytezos
from conseil import conseil
from conseil.api import ConseilApi
from tests import relpath
from tests.templates import operation_forging_test_case

Operation = conseil.tezos.babylonnet.operations

data_dir = join(dirname(dirname(__file__)), 'tests/operations')


def get_transaction_with_params(like, limit=1):
    return Operation.query(Operation.block_level, Operation.operation_group_hash) \
        .filter(Operation.kind == 'transaction',
                Operation.parameters.like(like),
                Operation.internal.is_(False)) \
        .limit(limit) \
        .all()


def get_origination_with_script(limit=1):
    return Operation.query(Operation.block_level, Operation.operation_group_hash) \
        .filter(Operation.kind == 'origination',
                Operation.script.isnot(None)) \
        .limit(limit) \
        .all()


def get_operation(kind, limit=1):
    return Operation.query(Operation.block_level, Operation.operation_group_hash) \
        .filter(Operation.kind == kind,
                Operation.parameters.is_(None),
                Operation.script.is_(None),
                Operation.internal.is_(False)) \
        .limit(limit) \
        .all()


def get_unsigned_data(block_level, operation_group_hash):
    return pytezos.shell.blocks[block_level].operations[operation_group_hash].unsigned()


def forge(block_level, unsigned_data):
    return pytezos.shell.blocks[block_level].helpers.forge.operations.post(unsigned_data)


def make_test(block_level, operation_group_hash):
    operation_dir = join(data_dir, operation_group_hash)
    if exists(operation_dir):
        return
    else:
        mkdir(operation_dir)

    unsigned_data = get_unsigned_data(block_level, operation_group_hash)
    json_path = join(operation_dir, 'unsigned.json')
    with open(json_path, 'w+') as f:
        f.write(json.dumps(unsigned_data, indent=2))

    expected = forge(block_level, unsigned_data)
    hex_path = join(operation_dir, 'forged.hex')
    with open(hex_path, 'w+') as f:
        f.write(expected)

    test_case = operation_forging_test_case.format(
        case=operation_group_hash[:6],
        json_path=relpath(json_path),
        hex_path=relpath(hex_path)
    )
    with open(join(operation_dir, f'test_forge_{operation_group_hash[:6]}.py'), 'w+') as f:
        f.write(test_case)


if __name__ == '__main__':
    for op_kind in ['activate_account', 'reveal', 'delegation', 'transaction', 'origination']:
        for data in get_operation(kind=op_kind, limit=5):
            make_test(**data)

    for term in ['int', 'bytes', 'Left', 'DIP', 'Elt']:
        for data in get_transaction_with_params(like='int', limit=5):
            make_test(**data)

    for data in get_origination_with_script(limit=150):
        make_test(**data)
