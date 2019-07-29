from pytezos.encoding import encode_address, encode_boolean, encode_nat, encode_with_len, encode_public_key, \
    encode_b58_value
from pytezos.michelson.forge import micheline_to_bytes, encode_script

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


def encode_operation(content):
    encode_content = {
        'activate_account': encode_activate_account,
        'reveal': encode_reveal,
        'transaction': encode_transaction,
        'origination': encode_origination,
        'delegation': encode_delegation
    }
    encode_proc = encode_content.get(content['kind'])
    if not encode_proc:
        raise NotImplementedError(content['kind'])

    return encode_proc(content)


def encode_operation_group(operation_group):
    res = encode_b58_value(operation_group['branch'])
    res += b''.join(map(encode_operation, operation_group['contents']))
    return res


def encode_activate_account(content: dict):
    res = encode_nat(operation_tags[content['kind']])
    res += encode_b58_value(content['pkh'])
    res += bytes.fromhex(content['secret'])
    return res


def encode_reveal(content):
    res = encode_nat(operation_tags[content['kind']])
    res += encode_address(content['source'])
    res += encode_nat(int(content['fee']))
    res += encode_nat(int(content['counter']))
    res += encode_nat(int(content['gas_limit']))
    res += encode_nat(int(content['storage_limit']))
    res += encode_public_key(content['public_key'])
    return res


def encode_transaction(content):
    res = encode_nat(operation_tags[content['kind']])
    res += encode_address(content['source'])
    res += encode_nat(int(content['fee']))
    res += encode_nat(int(content['counter']))
    res += encode_nat(int(content['gas_limit']))
    res += encode_nat(int(content['storage_limit']))
    res += encode_nat(int(content['amount']))
    res += encode_address(content['destination'])

    if content.get('parameters'):
        res += encode_boolean(True)
        res += encode_with_len(micheline_to_bytes(content['parameters']))
    else:
        res += encode_boolean(False)

    return res


def encode_origination(content):
    res = encode_nat(operation_tags[content['kind']])
    res += encode_address(content['source'])
    res += encode_nat(int(content['fee']))
    res += encode_nat(int(content['counter']))
    res += encode_nat(int(content['gas_limit']))
    res += encode_nat(int(content['storage_limit']))
    res += encode_address(content['manager_pubkey'])[1:]
    res += encode_nat(int(content['balance']))

    res += encode_boolean(content.get('spendable'))
    res += encode_boolean(content.get('delegatable'))

    if content.get('delegate'):
        res += encode_boolean(True)
        res += encode_address(content['delegate'])[1:]
    else:
        res += encode_boolean(False)
        
    if content.get('script'):
        res += encode_boolean(True)
        res += encode_script(content['script'])
    else:
        res += encode_boolean(False)

    return res


def encode_delegation(content):
    res = encode_nat(operation_tags[content['kind']])
    res += encode_address(content['source'])
    res += encode_nat(int(content['fee']))
    res += encode_nat(int(content['counter']))
    res += encode_nat(int(content['gas_limit']))
    res += encode_nat(int(content['storage_limit']))

    if content.get('delegate'):
        res += encode_boolean(True)
        res += encode_address(content['delegate'])[1:]
    else:
        res += encode_boolean(False)

    return res
