from os.path import join, dirname, exists
from os import mkdir
import json

from conseil import conseil
from conseil.api import ConseilApi
from pytezos import pytezos
from tests import relpath
from tests.templates import michelson_coding_test_case, micheline_coding_test_case, \
    test_michelson_parse,test_michelson_format, test_michelson_inverse, test_micheline_inverse

data_dir = join(dirname(dirname(__file__)), 'tests/contracts')

Account = conseil.tezos.alphanet.accounts
Operation = conseil.tezos.alphanet.operations


def get_accounts(limit=1):
    operations = Operation.query(Operation.destination,
                                 Operation.operation_group_hash.count()) \
        .filter(Operation.destination.startswith('KT1'),
                Operation.parameters.isnot(None),
                Operation.parameters.notlike('Unparsable'),
                Operation.kind == 'transaction',
                Operation.status == 'applied') \
        .order_by(Operation.operation_group_hash.count().desc()) \
        .limit(limit) \
        .all()

    addresses = list(map(lambda x: x['destination'], operations))

    accounts = Account.query(Account.account_id, Account.script, Account.storage) \
        .filter(Account.account_id.in_(*addresses),
                Account.storage.notlike('Unparsable'),
                Account.script.notlike('Unparsable')) \
        .all()

    return accounts


def get_operations(account_id, limit=1):
    operations = Operation.query(Operation.block_level.max().label('level'),
                                 Operation.parameters) \
        .filter(Operation.destination == account_id,
                Operation.parameters.isnot(None),
                Operation.parameters.notlike('Unparsable'),
                Operation.kind == 'transaction',
                Operation.status == 'applied',
                Operation.internal.is_(False)) \
        .limit(limit) \
        .all()

    return operations


def find_operation(block_level, destination):
    opg_list = pytezos.shell.blocks[block_level].operations.managers()
    for opg in opg_list:
        for content in opg['contents']:
            if content.get('parameters') and content['destination'] == destination:
                return content['parameters'], opg['hash']
    assert False


def make_package(account, operations=1):
    account_dir = join(data_dir, account["account_id"])
    if exists(account_dir):
        return
    else:
        mkdir(account_dir)

    files = {
        'dir': account_dir,
        'name': account['account_id'][:6],
        'code': [],
        'storage': [],
        'parameter': []
    }

    def write_files(michelson, micheline, section, name):
        tz_path = join(account_dir, f'{section}_{name}.tz')
        json_path = join(account_dir, f'{section}_{name}.json')

        with open(tz_path, 'w+') as f:
            f.write(michelson)

        with open(json_path, 'w+') as f:
            f.write(json.dumps(micheline, indent=2))

        files[section].append((name, tz_path, json_path))

    contract = pytezos.shell.contracts[account['account_id']]()
    write_files(
        michelson=account['script'],
        micheline=contract['script']['code'],
        section='code',
        name=account['account_id'][:6]
    )
    write_files(
        michelson=account['storage'],
        micheline=contract['script']['storage'],
        section='storage',
        name=account['account_id'][:6]
    )

    operations = get_operations(account['account_id'], limit=operations)
    for operation in operations:
        parameters, opg_hash = find_operation(operation['level'], account['account_id'])
        write_files(
            michelson=operation['parameters'],
            micheline=parameters,
            section='parameter',
            name=opg_hash[:6]
        )

    return files


def make_michelson_tests(files: dict):
    test_case = [
        michelson_coding_test_case.format(case=files['name'])
    ]

    for section in ['code', 'storage', 'parameter']:
        for name, tz_path, json_path in files[section]:
            case = f'{section}_{name}'
            test_case.extend([
                test_michelson_parse.format(case=case, json_path=relpath(json_path), tz_path=relpath(tz_path)),
                test_michelson_format.format(case=case, json_path=relpath(json_path), tz_path=relpath(tz_path)),
                test_michelson_inverse.format(case=case, json_path=relpath(json_path))
            ])

    with open(join(files['dir'], f'test_michelson_coding_{files["name"]}.py'), 'w+') as f:
        f.write(''.join(test_case))


def make_micheline_tests(files: dict):
    test_case = [
        micheline_coding_test_case.format(case=files['name'], json_path=relpath(files['code'][0][2]))
    ]

    for section in ['storage', 'parameter']:
        for name, tz_path, json_path in files[section]:
            case = f'{section}_{name}'
            test_case.append(
                test_micheline_inverse.format(case=case, json_path=relpath(json_path), section=section)
            )

    with open(join(files['dir'], f'test_micheline_coding_{files["name"]}.py'), 'w+') as f:
        f.write(''.join(test_case))


if __name__ == '__main__':
    accounts = get_accounts(limit=100)
    for acc in accounts:
        package = make_package(acc, operations=7)
        if package:
            make_michelson_tests(package)
            make_micheline_tests(package)
