from pytezos.encoding import forge_array, forge_address, forge_public_key, forge_timestamp, forge_contract, \
    forge_base58

prim_tags = {
    'parameter': b'\x00',
    'storage': b'\x01',
    'code': b'\x02',
    'False': b'\x03',
    'Elt': b'\x04',
    'Left': b'\x05',
    'None': b'\x06',
    'Pair': b'\x07',
    'Right': b'\x08',
    'Some': b'\x09',
    'True': b'\x0A',
    'Unit': b'\x0B',
    'PACK': b'\x0C',
    'UNPACK': b'\x0D',
    'BLAKE2B': b'\x0E',
    'SHA256': b'\x0F',
    'SHA512': b'\x10',
    'ABS': b'\x11',
    'ADD': b'\x12',
    'AMOUNT': b'\x13',
    'AND': b'\x14',
    'BALANCE': b'\x15',
    'CAR': b'\x16',
    'CDR': b'\x17',
    'CHECK_SIGNATURE': b'\x18',
    'COMPARE': b'\x19',
    'CONCAT': b'\x1A',
    'CONS': b'\x1B',
    '__CREATE_ACCOUNT__': b'\x1C',  # DEPRECATED
    'CREATE_CONTRACT': b'\x1D',
    'IMPLICIT_ACCOUNT': b'\x1E',
    'DIP': b'\x1F',
    'DROP': b'\x20',
    'DUP': b'\x21',
    'EDIV': b'\x22',
    'EMPTY_MAP': b'\x23',
    'EMPTY_SET': b'\x24',
    'EQ': b'\x25',
    'EXEC': b'\x26',
    'FAILWITH': b'\x27',
    'GE': b'\x28',
    'GET': b'\x29',
    'GT': b'\x2A',
    'HASH_KEY': b'\x2B',
    'IF': b'\x2C',
    'IF_CONS': b'\x2D',
    'IF_LEFT': b'\x2E',
    'IF_NONE': b'\x2F',
    'INT': b'\x30',
    'LAMBDA': b'\x31',
    'LE': b'\x32',
    'LEFT': b'\x33',
    'LOOP': b'\x34',
    'LSL': b'\x35',
    'LSR': b'\x36',
    'LT': b'\x37',
    'MAP': b'\x38',
    'MEM': b'\x39',
    'MUL': b'\x3A',
    'NEG': b'\x3B',
    'NEQ': b'\x3C',
    'NIL': b'\x3D',
    'NONE': b'\x3E',
    'NOT': b'\x3F',
    'NOW': b'\x40',
    'OR': b'\x41',
    'PAIR': b'\x42',
    'PUSH': b'\x43',
    'RIGHT': b'\x44',
    'SIZE': b'\x45',
    'SOME': b'\x46',
    'SOURCE': b'\x47',
    'SENDER': b'\x48',
    'SELF': b'\x49',
    'STEPS_TO_QUOTA': b'\x4A',
    'SUB': b'\x4B',
    'SWAP': b'\x4C',
    'TRANSFER_TOKENS': b'\x4D',
    'SET_DELEGATE': b'\x4E',
    'UNIT': b'\x4F',
    'UPDATE': b'\x50',
    'XOR': b'\x51',
    'ITER': b'\x52',
    'LOOP_LEFT': b'\x53',
    'ADDRESS': b'\x54',
    'CONTRACT': b'\x55',
    'ISNAT': b'\x56',
    'CAST': b'\x57',
    'RENAME': b'\x58',
    'bool': b'\x59',
    'contract': b'\x5A',
    'int': b'\x5B',
    'key': b'\x5C',
    'key_hash': b'\x5D',
    'lambda': b'\x5E',
    'list': b'\x5F',
    'map': b'\x60',
    'big_map': b'\x61',
    'nat': b'\x62',
    'option': b'\x63',
    'or': b'\x64',
    'pair': b'\x65',
    'set': b'\x66',
    'signature': b'\x67',
    'string': b'\x68',
    'bytes': b'\x69',
    'mutez': b'\x6A',
    'timestamp': b'\x6B',
    'unit': b'\x6C',
    'operation': b'\x6D',
    'address': b'\x6E',
    'SLICE': b'\x6F',
    'DIG': b'\x70',
    'DUG': b'\x71',
    'EMPTY_BIG_MAP': b'\x72',
    'APPLY': b'\x73',
    'chain_id': b'\x74',
    'CHAIN_ID': b'\x75'
}

len_tags = [
    {
        False: b'\x03',
        True: b'\x04'
    },
    {
        False: b'\x05',
        True: b'\x06'
    },
    {
        False: b'\x07',
        True: b'\x08'
    },
    {
        False: b'\x09',
        True: b'\x09'
    }
]

reserved_entries = {
    'default': b'\x00',
    'root': b'\x01',
    'do': b'\x02',
    'set_delegate': b'\x03',
    'remove_delegate': b'\x04'
}


def forge_int(value: int):
    res = bytearray()
    i = abs(value)

    res.append((i & 0b00111111) | (0b11000000 if value < 0 else 0b10000000))
    i >>= 6

    while i != 0:
        res.append((i & 0b01111111) | 0b10000000)
        i >>= 7

    res[-1] &= 0b01111111
    return bytes(res)


def forge_entrypoint(entrypoint):
    if entrypoint in reserved_entries:
        return reserved_entries[entrypoint]
    else:
        return b'\xff' + forge_array(entrypoint.encode(), len_bytes=1)


def forge_micheline(data):
    res = []

    if isinstance(data, list):
        res.append(b'\x02')
        res.append(forge_array(b''.join(map(forge_micheline, data))))

    elif isinstance(data, dict):
        if data.get('prim'):
            args_len = len(data.get('args', []))
            annots_len = len(data.get('annots', []))

            res.append(len_tags[args_len][annots_len > 0])
            res.append(prim_tags[data['prim']])

            if args_len > 0:
                args = b''.join(map(forge_micheline, data['args']))
                if args_len < 3:
                    res.append(args)
                else:
                    res.append(forge_array(args))

            if annots_len > 0:
                res.append(forge_array(' '.join(data['annots']).encode()))
            elif args_len == 3:
                res.append(b'\x00' * 4)

        elif data.get('bytes') is not None:
            res.append(b'\x0A')
            res.append(forge_array(bytes.fromhex(data['bytes'])))

        elif data.get('int') is not None:
            res.append(b'\x00')
            res.append(forge_int(int(data['int'])))

        elif data.get('string') is not None:
            res.append(b'\x01')
            res.append(forge_array(data['string'].encode()))
        else:
            assert False, data
    else:
        assert False, data

    return b''.join(res)


def forge_script(script):
    code = forge_micheline(script['code'])
    storage = forge_micheline(script['storage'])
    return forge_array(code) + forge_array(storage)


def prepack_micheline(val_expr, type_expr):
    def convert(val_node, type_node):
        prim = type_node['prim']
        is_string = isinstance(val_node, dict) and val_node.get('string')

        if prim in ['set', 'list']:
            return [
                prepack_micheline(item_node, type_node['args'][0])
                for item_node in val_node
            ]
        elif prim in ['map', 'big_map']:
            return [
                {'prim': 'Elt',
                 'args': [prepack_micheline(elt_node['args'][i], type_node['args'][i]) for i in [0, 1]]}
                for elt_node in val_node
            ]
        elif prim == 'pair':
            return [
                {'prim': 'Pair',
                 'args': [prepack_micheline(val_node['args'][i], type_node['args'][i]) for i in [0, 1]]}
            ]
        elif prim == 'option':
            if val_node['prim'] == 'Some':
                return {'prim': 'Some',
                        'args': [prepack_micheline(val_node['args'][0], type_node['args'][0])]}
            else:
                return val_node
        elif prim == 'or':
            idx = {'Left': 0, 'Right': 1}[val_node['prim']]
            return {'prim': val_node['prim'],
                    'args': [prepack_micheline(val_node['args'][0], type_node['args'][idx])]}
        elif prim == 'lambda':
            # TODO: PUSH, SELF, CONTRACT
            return val_node
        elif prim == 'chain_id' and is_string:
            return {'bytes': forge_base58(val_node['string']).hex()}
        elif prim == 'signature' and is_string:
            return {'bytes': forge_base58(val_node['string']).hex()}
        elif prim == 'key_hash' and is_string:
            return {'bytes': forge_address(val_node['string'], tz_only=True).hex()}
        elif prim == 'key' and is_string:
            return {'bytes': forge_public_key(val_node['string']).hex()}
        elif prim == 'address' and is_string:
            return {'bytes': forge_address(val_node['string']).hex()}
        elif prim == 'contract' and is_string:
            return {'bytes': forge_contract(val_node['string']).hex()}
        elif prim == 'timestamp' and is_string:
            return {'int': forge_timestamp(val_node['string'])}
        else:
            return val_node

    return convert(val_expr, type_expr)


def pack(val_expr, type_expr):
    data = prepack_micheline(val_expr, type_expr)
    return b'\x05' + forge_micheline(data)
