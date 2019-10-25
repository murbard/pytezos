import json
from os.path import join, dirname, exists
from os import mkdir

from pytezos import pytezos
from conseil import conseil
from conseil.api import ConseilApi
from tests import relpath
from tests.templates import big_map_test_case

Operation = conseil.tezos.babylonnet.operations

data_dir = join(dirname(dirname(__file__)), 'tests/big_map_diff')


def get_transaction_with_big_map_diff(limit=1):
    return Operation.query(Operation.block_level, Operation.operation_group_hash) \
        .filter(Operation.kind == 'transaction',
                Operation.paid_storage_size_diff > 20,
                Operation.parameters.isnot(None),
                Operation.internal.is_(False)) \
        .limit(limit) \
        .all()


def make_test(block_level, operation_group_hash):
    operation_dir = join(data_dir, operation_group_hash)
    if exists(operation_dir):
        return
    else:
        mkdir(operation_dir)

    opg = pytezos.shell.blocks[block_level].operations[operation_group_hash]()
    content = opg['contents'][0]
    try:
        big_map_diff = content['metadata']['operation_result']['big_map_diff']
    except (KeyError, IndexError, TypeError):
        return

    diff_path = join(operation_dir, 'big_map_diff.json')
    with open(diff_path, 'w+') as f:
        f.write(json.dumps(big_map_diff, indent=2))

    script = pytezos.shell.contracts[content['destination']]().get('script')
    code_path = join(operation_dir, 'storage_section.json')
    with open(code_path, 'w+') as f:
        f.write(json.dumps(script['code'][1], indent=2))

    test_case = big_map_test_case.format(
        case=operation_group_hash[:6],
        code_path=relpath(code_path),
        diff_path=relpath(diff_path)
    )
    with open(join(operation_dir, f'test_big_map_{operation_group_hash[:6]}.py'), 'w+') as f:
        f.write(test_case)


if __name__ == '__main__':
    if not exists(data_dir):
        mkdir(data_dir)

    for data in get_transaction_with_big_map_diff(limit=400):
        make_test(**data)
