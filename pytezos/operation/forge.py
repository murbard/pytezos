from pytezos.encoding import forge_address, forge_bool, forge_nat, forge_array, forge_public_key, \
    forge_base58
from pytezos.michelson.forge import forge_micheline, forge_script

# TODO: https://tezos.gitlab.io/master/protocols/005_PsBABY5H.html#changes-to-the-binary-format-of-operations

operation_tags = {
    'endorsement': 0,
    'proposal': 5,
    'ballot': 6,
    'seed_nonce_revelation': 1,
    'double_endorsement_evidence': 2,
    'double_baking_evidence': 3,
    'activate_account': 4,
    'reveal': 7,
    'transaction': 8,
    'origination': 9,
    'delegation': 10
}


def forge_operation(content):
    encode_content = {
        'activate_account': forge_activate_account,
        'reveal': forge_reveal,
        'transaction': forge_transaction,
        'origination': forge_origination,
        'delegation': forge_delegation
    }
    encode_proc = encode_content.get(content['kind'])
    if not encode_proc:
        raise NotImplementedError(content['kind'])

    return encode_proc(content)


def forge_operation_group(operation_group):
    res = forge_base58(operation_group['branch'])
    res += b''.join(map(forge_operation, operation_group['contents']))
    return res


def forge_activate_account(content: dict):
    res = forge_nat(operation_tags[content['kind']])
    res += forge_base58(content['pkh'])
    res += bytes.fromhex(content['secret'])
    return res


def forge_reveal(content):
    res = forge_nat(operation_tags[content['kind']])
    res += forge_address(content['source'])
    res += forge_nat(int(content['fee']))
    res += forge_nat(int(content['counter']))
    res += forge_nat(int(content['gas_limit']))
    res += forge_nat(int(content['storage_limit']))
    res += forge_public_key(content['public_key'])
    return res


def forge_transaction(content):
    res = forge_nat(operation_tags[content['kind']])
    res += forge_address(content['source'])
    res += forge_nat(int(content['fee']))
    res += forge_nat(int(content['counter']))
    res += forge_nat(int(content['gas_limit']))
    res += forge_nat(int(content['storage_limit']))
    res += forge_nat(int(content['amount']))
    res += forge_address(content['destination'])

    if content.get('parameters'):
        res += forge_bool(True)
        res += forge_array(forge_micheline(content['parameters']))
    else:
        res += forge_bool(False)

    return res


def forge_origination(content):
    res = forge_nat(operation_tags[content['kind']])
    res += forge_address(content['source'])
    res += forge_nat(int(content['fee']))
    res += forge_nat(int(content['counter']))
    res += forge_nat(int(content['gas_limit']))
    res += forge_nat(int(content['storage_limit']))
    res += forge_address(content.get('manager_pubkey', content.get('managerPubkey')), tz_only=True)
    res += forge_nat(int(content['balance']))

    no_script = 'script' not in content
    res += forge_bool(content.get('spendable', no_script))
    res += forge_bool(content.get('delegatable', no_script))

    if content.get('delegate'):
        res += forge_bool(True)
        res += forge_address(content['delegate'], tz_only=True)
    else:
        res += forge_bool(False)
        
    if content.get('script'):
        res += forge_bool(True)
        res += forge_script(content['script'])
    else:
        res += forge_bool(False)

    return res


def forge_delegation(content):
    res = forge_nat(operation_tags[content['kind']])
    res += forge_address(content['source'])
    res += forge_nat(int(content['fee']))
    res += forge_nat(int(content['counter']))
    res += forge_nat(int(content['gas_limit']))
    res += forge_nat(int(content['storage_limit']))

    if content.get('delegate'):
        res += forge_bool(True)
        res += forge_address(content['delegate'], tz_only=True)
    else:
        res += forge_bool(False)

    return res
