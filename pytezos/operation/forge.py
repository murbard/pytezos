import base58
import json


OPERATION_TYPES = [
    "endorsement",
    "seedNonceRevelation",
    "doubleEndorsementEvidence",
    "doubleBakingEvidence",
    "accountActivation",
    "proposal",
    "ballot",
    "reveal",
    "transaction",
    "origination",
    "delegation"
]

PRIM_MAPPING_REVERSE = [
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

OPERATION_MAPPING = {
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
  'SLICE': b'\x6F'
}


def encode_reveal(operation):
    if operation.get("kind") != "reveal":
        raise ValueError("Incorrect operation type")

    decoded = write_int(OPERATION_TYPES.index("reveal"))
    decoded += write_address(operation["source"])
    decoded += write_int(int(operation["fee"]))
    decoded += write_int(int(operation["counter"]))
    decoded += write_int(int(operation["gas_limit"]))
    decoded += write_int(int(operation["storage_limit"]))
    decoded += write_public_key(operation["public_key"])

    return decoded


def encode_transaction(operation):
    if operation.get("kind") != "transaction":
        raise ValueError("Incorrect operation type")

    decoded = write_int(OPERATION_TYPES.index("transaction"))
    decoded += write_address(operation["source"])
    decoded += write_int(int(operation["fee"]))
    decoded += write_int(int(operation["counter"]))
    decoded += write_int(int(operation["gas_limit"]))
    decoded += write_int(int(operation["storage_limit"]))
    decoded += write_int(int(operation["amount"]))
    decoded += write_address(operation["destination"])
    
    if operation.get("parameters"):
        decoded += write_boolean(True)
        result = write_json(json.loads(operation["parameters"]))
        decoded += len(result).to_bytes(4, 'big') + result
    else:
        decoded += write_boolean(False)
    
    return decoded


def encode_origination(operation):
    if operation.get("kind") != "origination":
        raise ValueError("Incorrect operation type")

    decoded = write_int(OPERATION_TYPES.index("origination"))
    decoded += write_address(operation["source"])
    decoded += write_int(int(operation["fee"]))
    decoded += write_int(int(operation["counter"]))
    decoded += write_int(int(operation["gas_limit"]))
    decoded += write_int(int(operation["storage_limit"]))
    decoded += write_address(operation["manager_pubkey"])[1:]
    decoded += write_int(int(operation["balance"]))
    
    decoded += write_boolean(operation.get('spendable'))
    decoded += write_boolean(operation.get('delegatable'))

    if operation.get("delegate"):
        decoded += write_boolean(True)
        decoded += write_address(operation["delegate"])[1:]
    else:
        decoded += write_boolean(False)
        
    if operation.get("script"):
        decoded += write_boolean(True)
        decoded += write_script(json.loads(operation["script"]))
    else:
        decoded += write_boolean(False)

    return decoded


def encode_delegation(operation):
    if operation.get("kind") != "delegation":
        raise ValueError("Incorrect operation type")

    decoded = write_int(OPERATION_TYPES.index("delegation"))
    decoded += write_address(operation["source"])
    decoded += write_int(int(operation["fee"]))
    decoded += write_int(int(operation["counter"]))
    decoded += write_int(int(operation["gas_limit"]))
    decoded += write_int(int(operation["storage_limit"]))

    if operation.get("delegate"):
        decoded += write_boolean(True)
        decoded += write_address(operation["delegate"])[1:]
    else:
        decoded += write_boolean(False)

    return decoded


def write_int(value):
    """
    Encode a number using LEB128 encoding.
    :param int value: the value to encode
    :return: encoded value
    :rtype: bytes
    """

    if value < 0:
        raise ValueError("Value cannot be negative.")

    buf = bytearray()
    more = True

    while more:
        # Obtain the lowest 7 bits, and shift the remainder.
        byte = value & 0x7f
        value >>= 7

        if value:
            # Not done yet
            byte |= 0x80
        else:
            more = False

        buf.append(byte)

    return bytes(buf)


def write_public_key(value):
    prefix = value[:4]
    decoded = base58.b58decode_check(value)[4:]

    if prefix == "edpk":
        return b"\x00" + decoded
    elif prefix == "sppk":
        return b"\x01" + decoded
    elif prefix == "p2pk":
        return b"\x02" + decoded
    
    raise ValueError(f"Unrecognized key type: #{prefix}")


def write_address(value):
    prefix = value[:3]
    decoded = base58.b58decode_check(value)[3:]

    if prefix == "tz1":
        return b"\x00\x00" + decoded
    elif prefix == "tz2":
        return b"\x00\x01" + decoded
    elif prefix == "tz3":
        return b"\x00\x02" + decoded
    elif prefix == "KT1":
        return b"\x01" + decoded + b"\x00"

    raise ValueError(f"Unrecognized address prefix: #{prefix}")


def write_boolean(value):
    if value == "true":
        return b"\xff"
    elif value == True:
        return b"\xff"

    return b"\x00"


def write_script(script):
    code = write_json(script["code"])
    storage = write_json(script["storage"])
    return len(code).to_bytes(4, 'big') + code + len(storage).to_bytes(4, 'big') + storage


def write_json(data):
    def encode_node(data):
        result = []
        
        if isinstance(data, list):
            list_bytes = b''.join([encode_node(arg) for arg in data])
            result.append(b"\x02")
            result.append(len(list_bytes).to_bytes(4, byteorder="big"))
            result.append(list_bytes)
        elif isinstance(data, dict):
            if data.get("prim"):
                args_len = len(data["args"]) if data.get("args") else 0
                result.append(PRIM_MAPPING_REVERSE[args_len][data.get("annots") != None])
                result.append(OPERATION_MAPPING[data["prim"]])

                if data.get("args"):
                    args_bytes = [encode_node(arg) for arg in data["args"]]
                    result.append(b''.join(args_bytes))
                
                if data.get("annots"):
                    annots = [annot.encode() for annot in data["annots"]]
                    annots_bytes = b' '.join(annots)
                    result.append(len(annots_bytes).to_bytes(4, 'big'))
                    result.append(annots_bytes)

            elif data.get("bytes"):
                result.append(b'\x0A')
                result.append(len(bytes.fromhex(data["bytes"])).to_bytes(4, 'big'))
                result.append(bytes.fromhex(data["bytes"]))
            elif data.get("int"):
                num = int(data["int"])
                mark = '0' if num >= 0 else '1'
                binary = format(num, "b")
                pad = 0

                if (len(binary) - 6) % 7 == 0:
                    pad = len(binary)
                elif len(binary) <= 6:
                    pad = 6
                else:
                    pad = len(binary) + 7 - (len(binary) - 6) % 7

                s = binary.zfill(pad)
                splitted = [s[i:i+7] for i in range(0, len(s), 7)]
                sp_reversed = splitted[::-1]
                sp_reversed[0] = mark + sp_reversed[0]

                res = []
                for idx in range(len(sp_reversed)):
                    prefix = '0' if idx == len(sp_reversed) - 1 else '1'
                    sstr = prefix + sp_reversed[idx]
                    res.append(int(sstr, 2).to_bytes(1, 'big'))

                result.append(b'\x00')
                result.append(b''.join(res))

            elif data.get("string"):
                result.append(b'\x01')
                data_string = data["string"].encode()
                result.append(len(data_string).to_bytes(4, 'big'))
                result.append(data_string)

        return b''.join(result)

    return encode_node(data)
