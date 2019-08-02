from pytezos.encoding import forge_array

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
  'CREATE_ACCOUNT': b'\x1C',
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
  'michelson': b'\x5A',
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
  'SLICE': b'\x6F'
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
        True: b'\x09'
    }
]


def forge_int(value: int):
    mark = '0' if value >= 0 else '1'
    binary = format(value, 'b')

    if (len(binary) - 6) % 7 == 0:
        pad = len(binary)
    elif len(binary) <= 6:
        pad = 6
    else:
        pad = len(binary) + 7 - (len(binary) - 6) % 7

    s = binary.zfill(pad)
    splitted = [s[i:i + 7] for i in range(0, len(s), 7)]
    sp_reversed = splitted[::-1]
    sp_reversed[0] = mark + sp_reversed[0]

    res = []
    for idx in range(len(sp_reversed)):
        prefix = '0' if idx == len(sp_reversed) - 1 else '1'
        sstr = prefix + sp_reversed[idx]
        res.append(int(sstr, 2).to_bytes(1, 'big'))

    return b''.join(res)


def micheline_to_bytes(data):
    res = []

    if isinstance(data, list):
        res.append(b'\x02')
        res.append(forge_array(b''.join(map(micheline_to_bytes, data))))

    elif isinstance(data, dict):
        if data.get('prim'):
            args_len = len(data.get('args', []))
            annots_len = len(data.get('annots', []))

            res.append(len_tags[args_len][annots_len > 0])
            res.append(prim_tags[data['prim']])

            if args_len > 0:
                res.append(b''.join(map(micheline_to_bytes, data['args'])))

            if annots_len > 0:
                res.append(forge_array(b' '.join(map(lambda x: x.encode(), data['annots']))))

        elif data.get('bytes'):
            res.append(b'\x0A')
            res.append(forge_array(bytes.fromhex(data['bytes'])))

        elif data.get('int'):
            res.append(b'\x00')
            res.append(forge_int(int(data['int'])))

        elif data.get('string'):
            res.append(b'\x01')
            res.append(forge_array(data['string'].encode()))
        else:
            raise NotImplementedError(data)
    else:
        raise ValueError(data)

    return b''.join(res)


def forge_script(script):
    code = micheline_to_bytes(script['code'])
    storage = micheline_to_bytes(script['storage'])
    return forge_array(code) + forge_array(storage)
