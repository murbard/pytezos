import re
from typing import Dict
from datetime import datetime
from os.path import join, dirname, basename
from decimal import Decimal
from collections import namedtuple, defaultdict
from functools import lru_cache

from pytezos.encoding import parse_address, parse_public_key, forge_public_key, forge_address, forge_base58
from pytezos.michelson.grammar import MichelsonParser
from pytezos.michelson.formatter import format_node

Nested = namedtuple('Nested', ['prim', 'args'])
Schema = namedtuple('Schema', ['metadata', 'bin_types', 'bin_to_json', 'json_to_bin'])

meaningful_types = ['key', 'key_hash', 'signature', 'timestamp', 'address']
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


@lru_cache(maxsize=None)
def michelson_parser():
    return MichelsonParser()


def to_snake_case(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def decode_literal(node, prim):
    core_type, value = next(iter(node.items()))
    if prim in ['int', 'nat']:
        return int(value)
    if prim == 'timestamp':
        if core_type == 'int':
            return int(value)
        else:
            return value
    if prim == 'mutez':
        return Decimal(value) / 10 ** 6
    if prim == 'bool':
        return value == 'True'
    if core_type == 'bytes':
        if prim in ['address', 'key_hash', 'contract']:
            return parse_address(bytes.fromhex(value))
        if prim == 'key':
            return parse_public_key(bytes.fromhex(value))
    return value


def encode_literal(value, prim, binary=False):
    core_type = 'string'
    if prim in ['int', 'nat']:
        core_type = 'int'
    elif prim == 'timestamp':
        if isinstance(value, int):
            core_type = 'int'
        elif isinstance(value, datetime):
            value = value.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif prim == 'mutez':
        core_type = 'int'
        if isinstance(value, Decimal):
            value = int(value * 10 ** 6)
    elif prim == 'bool':
        core_type = 'prim'
        value = 'True' if value else 'False'
    elif prim == 'bytes':
        if isinstance(value, bytes):
            value = value.hex()
        core_type = 'bytes'
    elif binary:
        if prim == 'key':
            value = forge_public_key(value).hex()
            core_type = 'bytes'
        elif prim in ['address', 'contract', 'key_hash']:
            value = forge_address(value, tz_only=prim == 'key_hash').hex()
            core_type = 'bytes'

    return {core_type: str(value)}


def get_flat_nested(nested: Nested):
    flat_args = list()
    for arg in nested.args:
        if isinstance(arg, Nested) and arg.prim == nested.prim:
            flat_args.extend(get_flat_nested(arg))
        else:
            flat_args.append(arg)
    return flat_args


def make_dict(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v}


def collapse_micheline(code) -> dict:
    metadata = dict()

    def get_annotation(x, prefix, default=None):
        return next((a[1:] for a in x.get('annots', []) if a[0] == prefix), default)

    def parse_node(node, path='0', parent_prim=None, entry=None):
        if node['prim'] in ['storage', 'parameter']:
            return parse_node(node['args'][0])

        fieldname = get_annotation(node, '%')
        typename = get_annotation(node, ':')

        metadata[path] = make_dict(
            prim=node['prim'],
            typename=typename,
            fieldname=fieldname,
            entry=entry
        )

        if node['prim'] == 'option':
            return parse_node(
                node=node['args'][0],
                path=path + '0',
                parent_prim=parent_prim,
                entry=fieldname
            )
        elif node['prim'] in ['lambda', 'contract']:
            metadata[path]['parameter'] = micheline_to_michelson(node['args'][0], inline=True)
            return dict(path=path, args=[])  # stop there

        args = [
            parse_node(arg, path=path + str(i), parent_prim=node['prim'])
            for i, arg in enumerate(node.get('args', []))
        ]

        if node['prim'] in ['pair', 'or']:
            res = Nested(node['prim'], args)
            is_struct = node['prim'] == 'pair' and (typename or fieldname)
            if is_struct or parent_prim != node['prim']:
                args = get_flat_nested(res)
            else:
                return res

        if args:
            metadata[path]['args'] = list(map(lambda x: x['path'], args))

        return dict(path=path, args=args)

    parse_node(code)
    return metadata


def build_maps(metadata: dict):
    bin_types = {k: v['prim'] for k, v in metadata.items()}
    bin_to_json, json_to_bin = {}, {}

    def is_unit(bin_path):
        node = metadata[bin_path]
        return node.get('prim') == 'unit'

    def get_entry(bin_path):
        node = metadata[bin_path]
        entry = node.get('entry', node.get('fieldname', node.get('typename')))
        return to_snake_case(entry.replace('_Liq_entry_', '')) if entry else None

    def get_lr_path(bin_path):
        entry = ''
        for i in range(len(bin_path) - 1, 0, -1):
            lpath = bin_path[:i]
            if bin_types[lpath] in ['or', 'enum', 'router']:
                entry = {'0': 'l', '1': 'r'}[bin_path[i]] + entry
            else:
                return entry
        assert entry, bin_path
        return entry

    def get_key(bin_path):
        node = metadata[bin_path]
        default = node['prim'] if node['prim'] in meaningful_types else None
        key = node.get('typename', node.get('fieldname', node.get('entry', default)))
        return to_snake_case(key) if key else None

    def parse_node(bin_path='0', json_path='/'):
        node = metadata[bin_path]

        if node['prim'] in ['list', 'set', 'map', 'big_map']:
            index = 0 if node['prim'] in ['list', 'set'] else 1
            parse_node(node['args'][index], join(json_path, '{}'))

        elif node['prim'] == 'or':
            entries = list(map(get_entry, node['args']))
            named = all(entries) and len(entries) == len(set(entries))

            if all(map(is_unit, node['args'])):
                bin_types[bin_path] = 'enum'
                for i, arg in enumerate(node['args']):
                    bin_types[arg] = entries[i] if named else str(i)
                    parse_node(arg, join(json_path, bin_types[arg]))
            else:
                if not named:
                    entries = list(map(get_lr_path, node['args']))

                bin_types[bin_path] = 'router'
                for i, arg in enumerate(node['args']):
                    parse_node(arg, join(json_path, entries[i]))

        elif node['prim'] == 'pair':
            keys = list(map(get_key, node['args']))
            named = all(keys) and len(keys) == len(set(keys))

            bin_types[bin_path] = 'namedtuple' if named else 'tuple'
            for i, arg in enumerate(node['args']):
                parse_node(arg, join(json_path, keys[i] if named else str(i)))

        bin_to_json[bin_path], json_to_bin[json_path] = json_path, bin_path

    parse_node()
    return bin_types, bin_to_json, json_to_bin


def parse_micheline(data, bin_to_json: dict, bin_types: dict, bin_root='0'):
    json_values = dict()
    wild_root = bin_to_json[bin_root]

    def get_json_path(bin_path, params: list):
        wild_path = bin_to_json.get(bin_path)
        if wild_root != '/' and wild_path.startswith(wild_root):
            wild_path = join('/', wild_path[len(wild_root):])

        return wild_path.format(*params)

    def set_value(bin_path, params: list, value):
        json_path = get_json_path(bin_path, params)
        json_values[json_path] = value

    def parse_node(node, bin_path, params):
        bin_type = bin_types[bin_path]
        if bin_type in ['map', 'big_map', 'namedtuple', 'router']:
            set_value(bin_path, params, dict())
        elif bin_type in ['list', 'set', 'tuple']:
            set_value(bin_path, params, list())

        if isinstance(node, dict):
            if node.get('prim') == 'Pair':
                for i, arg in enumerate(node['args']):
                    parse_node(arg, bin_path + str(i), params)
            elif node.get('prim') == 'Left':
                parse_node(node['args'][0], bin_path + '0', params)
            elif node.get('prim') == 'Right':
                parse_node(node['args'][0], bin_path + '1', params)
            elif node.get('prim') == 'Elt':
                assert False  # should be already handled
            elif node.get('prim') == 'Some':
                parse_node(node['args'][0], bin_path + '0', params)
            elif node.get('prim') == 'None':
                set_value(bin_path + '0', params, None)
            elif node.get('prim') == 'Unit':
                if bin_type == 'unit':
                    set_value(bin_path, params, None)
                else:
                    json_path = dirname(get_json_path(bin_path, params))
                    json_values[json_path] = bin_type
            else:
                set_value(bin_path, params, decode_literal(node, bin_types[bin_path]))

        elif isinstance(node, list):
            if bin_type in ['map', 'big_map']:
                for elt in node:
                    key = decode_literal(elt['args'][0], bin_types[bin_path + '0'])
                    parse_node(elt['args'][1], bin_path + '1', params + [key])
            elif bin_type in ['set', 'list']:
                for i, arg in enumerate(node):
                    parse_node(arg, bin_path + '0', params + [i])
            elif bin_type == 'lambda':
                set_value(bin_path, params, micheline_to_michelson(node))
            else:
                assert False, (node, bin_path)
        else:
            assert False, (node, bin_path)

    parse_node(data, bin_root, [])
    return json_values


def make_json(json_values: dict):
    root = json_values['/']
    if type(root) in [dict, list]:
        tree = root.copy()
    else:
        return root

    def get_parent_node(path):
        node = tree
        keys = dirname(path).split('/')
        for key in keys:
            if not key:
                continue
            if isinstance(node, list):
                node = node[int(key)]
            else:
                node = node[key]
        return node

    for json_path, value in json_values.items():
        if json_path == '/':
            continue
        if type(value) in [dict, list]:
            value = value.copy()

        parent_node = get_parent_node(json_path)
        key_path = basename(json_path)
        if isinstance(parent_node, list):
            parent_node.insert(int(key_path), value)
        else:
            parent_node[key_path] = value

    return tree


def parse_json(data, json_to_bin: dict, bin_types: dict, json_root='/'):
    bin_values = defaultdict(dict)  # type: Dict[str, dict]

    def parse_entry(bin_path, index):
        for i in range(len(bin_path) - 1, 0, -1):
            lpath = bin_path[:i]
            if bin_types[lpath] in ['or', 'router', 'enum']:
                bin_values[lpath][index] = bin_path[i]
            elif bin_types[lpath] in ['list', 'set', 'map', 'big_map']:
                return

    def parse_node(node, json_path, index='0'):
        bin_path = json_to_bin[json_path]
        bin_type = bin_types[bin_path]

        if isinstance(node, dict):
            if bin_type in ['map', 'big_map']:
                bin_values[bin_path][index] = len(node)
                parse_entry(bin_path, index)
                for i, (key, value) in enumerate(node.items()):
                    bin_values[bin_path + '0'][f'{index}:{i}'] = key
                    parse_node(value, join(json_path, '{}'), f'{index}:{i}')

            elif bin_type in ['pair', 'or', 'namedtuple', 'router']:
                for key, value in node.items():
                    parse_node(value, join(json_path, key), index)
            else:
                assert False, (node, json_path)

        elif isinstance(node, list):
            if bin_type in ['list', 'set']:
                bin_values[bin_path][index] = len(node)
                parse_entry(bin_path, index)
                for i, value in enumerate(node):
                    parse_node(value, join(json_path, '{}'), f'{index}:{i}')

            elif bin_type in ['pair', 'tuple']:
                for i, value in enumerate(node):
                    parse_node(value, join(json_path, str(i)), index)

            elif bin_type == 'lambda':
                bin_values[bin_path][index] = node

            elif bin_type == 'or':
                assert False, (node, bin_path)  # must be at least lr encoded
        else:
            if bin_type == 'enum':
                parse_node(node, join(json_path, node), index)
            else:
                bin_values[bin_path][index] = node
                parse_entry(bin_path, index)

    parse_node(data, json_root)
    return dict(bin_values)


def make_micheline(bin_values: dict, bin_types: dict, bin_root='0', binary=False):

    def get_length(bin_path, index):
        try:
            length = bin_values[bin_path][index]
        except KeyError:
            length = 0  # TODO: make sure there is an option ahead
        return length

    def encode_node(bin_path, index='0'):
        bin_type = bin_types[bin_path]

        if bin_type in ['pair', 'tuple', 'namedtuple']:
            return dict(
                prim='Pair',
                args=list(map(lambda x: encode_node(bin_path + x, index), '01'))
            )
        elif bin_type in ['map', 'big_map']:
            length = get_length(bin_path, index)
            return [
                dict(
                    prim='Elt',
                    args=[encode_node(bin_path + '0', f'{index}:{i}'),
                          encode_node(bin_path + '1', f'{index}:{i}')]
                )
                for i in range(length)
            ]
        elif bin_type in ['set', 'list']:
            length = get_length(bin_path, index)
            return [
                encode_node(bin_path + '0', f'{index}:{i}')
                for i in range(length)
            ]
        elif bin_type in ['or', 'router', 'enum']:
            entry = bin_values[bin_path][index]
            return dict(
                prim={'0': 'Left', '1': 'Right'}[entry],
                args=[encode_node(bin_path + entry, index)]
            )
        elif bin_type == 'option':
            try:
                value = encode_node(bin_path + '0', index)
                if value:
                    return dict(prim='Some', args=[value])
                else:
                    return dict(prim='None')
            except KeyError:
                return dict(prim='None')
        elif bin_type == 'lambda':
            return michelson_to_micheline(bin_values[bin_path][index])
        elif bin_type == 'unit':
            return dict(prim='Unit')
        else:
            value = bin_values[bin_path][index]
            if value == bin_type:
                return dict(prim='Unit')
            elif value is None:
                return None
            else:
                return encode_literal(value, bin_type, binary)

    return encode_node(bin_root)


def make_default(bin_types: dict, root='0'):

    def encode_node(bin_path):
        bin_type = bin_types[bin_path]
        if bin_type == 'option':
            return dict(prim='None')
        elif bin_type in ['pair', 'tuple', 'namedtuple']:
            return dict(
                prim='Pair',
                args=list(map(lambda x: encode_node(bin_path + x), '01'))
            )
        elif bin_type in ['map', 'big_map', 'set', 'list']:
            return []
        elif bin_type in ['int', 'nat', 'mutez', 'timestamp']:
            return {'int': 0}
        elif bin_type in ['string', 'bytes']:
            return {'string': ''}
        elif bin_type == 'bool':
            return {'prim': 'False'}
        elif bin_type == 'unit':
            return {'prim': 'Unit'}
        else:
            raise ValueError(f'Cannot create default value for `{bin_type}` at `{bin_path}`')

    return encode_node(root)


def build_schema(code) -> Schema:
    """
    Creates internal structures necessary for decoding/encoding micheline:
    `metadata` -> micheline tree with collapsed `pair`, `or`, and `option` nodes
    `bin_types` -> maps binary path to primitive
    `bin_to_json` -> binary path to json path mapping
    `json_to_bin` -> reversed `bin_to_json`
    :param code: parameter or storage section of smart contract source code (in micheline)
    :return: Schema
    """
    metadata = collapse_micheline(code)
    return Schema(metadata, *build_maps(metadata))


def decode_micheline(data, schema: Schema, root='0'):
    """
    Converts Micheline data into Python object
    :param data: Micheline expression
    :param schema: schema built for particular contract/section
    :param root: which binary node to take as root, used to decode BigMap values/diffs
    :return: Object
    """
    json_values = parse_micheline(data, schema.bin_to_json, schema.bin_types, root)
    return make_json(json_values)


def encode_micheline(data, schema: Schema, root='0', binary=False):
    """
    Converts Python object into Micheline expression
    :param data: Python object
    :param schema: schema built for particular contract/section
    :param root: which binary node to take as root, used to encode BigMap values
    :param binary: Encode keys and addresses in bytes rather than strings, default is False
    :return: Micheline expression
    """
    json_root = schema.bin_to_json[root]
    bin_values = parse_json(data, schema.json_to_bin, schema.bin_types, json_root)
    return make_micheline(bin_values, schema.bin_types, root, binary)


def michelson_to_micheline(data):
    """
    Converts michelson source text into Micheline expression
    :param data: Michelson string
    :return: Micheline expression
    """
    return michelson_parser().parse(data)


def micheline_to_michelson(data, inline=False):
    """
    Converts micheline expression into formatted Michelson source
    :param data: Micheline expression
    :param inline: produce single line, used for tezos-client arguments (False by default)
    :return: string
    """
    return format_node(data, inline=inline, is_root=True)
