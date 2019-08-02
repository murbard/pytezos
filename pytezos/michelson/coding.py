import pendulum
import re
from datetime import datetime
from os.path import join
from decimal import Decimal
from collections import namedtuple, defaultdict

from pytezos.encoding import parse_address, parse_public_key

Nested = namedtuple('Nested', ['prim', 'args'])
Schema = namedtuple('Schema', ['bin_types', 'bin_to_json', 'json_types', 'json_to_bin'])

meaningful_types = ['key', 'key_hash', 'signature', 'timestamp', 'address']
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def to_snake_case(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def decode_literal(node, prim):
    core_type, value = next(iter(node.items()))
    if prim in ['int', 'nat']:
        return int(value)
    if prim == 'timestamp':
        if core_type == 'int':
            return pendulum.from_timestamp(int(value))
        else:
            return pendulum.parse(value)
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


def encode_literal(value, prim):
    if prim in ['int', 'nat']:
        core_type = 'int'
        value = str(value)
    elif prim == 'timestamp':
        core_type = 'string'
        if isinstance(value, int):
            value = pendulum.from_timestamp(value)
        if isinstance(value, pendulum.DateTime) or isinstance(value, datetime):
            value = value.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif prim == 'mutez':
        core_type = 'int'
        if isinstance(value, Decimal):
            value = int(value * 10 ** 6)
        if isinstance(value, int):
            value = str(value)
    elif prim == 'bool':
        core_type = 'prim'
        value = 'True' if value else 'False'
    elif prim == 'bytes':
        core_type = 'bytes'
    else:
        core_type = 'string'
        value = str(value)

    return {core_type: value}


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

        args = [
            parse_node(arg, path=path + str(i), parent_prim=node['prim'])
            for i, arg in enumerate(node.get('args', []))
        ]

        if node['prim'] in ['pair', 'or']:
            res = Nested(node['prim'], args)
            if typename or parent_prim != node['prim']:
                args = get_flat_nested(res)
            else:
                return res

        if args:
            metadata[path]['args'] = list(map(lambda x: x['path'], args))

        return dict(path=path, args=args)

    parse_node(code)
    return metadata


def build_maps(metadata: dict):
    json_types = {}
    bin_to_json = {}

    def get_entry(bin_path):
        node = metadata[bin_path]
        entry = node.get('entry', node.get('fieldname', node.get('typename')))
        return to_snake_case(entry.replace('_Liq_entry_', '')) if entry else None

    def get_key(bin_path, entry=None):
        node = metadata[bin_path]
        default = node['prim'] if node['prim'] in meaningful_types else None
        for key in [node.get('typename'), node.get('fieldname'), default]:
            if key:
                key = to_snake_case(key)
                return key if key != entry else None

    def parse_node(bin_path='0', json_path='/', entry=None):
        node = metadata[bin_path]

        if node['prim'] in ['list', 'set']:
            json_types[json_path] = 'list'
            parse_node(node['args'][0], join(json_path, '{}'))

        elif node['prim'] in ['map', 'big_map']:
            json_types[json_path] = 'dict'
            parse_node(node['args'][1], join(json_path, '{}'))

        elif node['prim'] == 'pair':
            keys = list(map(get_key, node['args']))
            named = all(keys) and len(keys) == len(set(keys))
            json_types[json_path] = 'dict' if named else 'list'
            for i, arg in enumerate(node['args']):
                parse_node(arg, join(json_path, keys[i] if named else str(i)))

        elif node['prim'] == 'or':
            entries = list(map(get_entry, node['args']))
            named = all(entries) and len(entries) == len(set(entries))
            json_types[json_path] = 'dict' if named else 'list'
            for i, arg in enumerate(node['args']):
                entrypoint = entries[i] if named else str(i)
                parse_node(arg, join(json_path, entrypoint), entry=entrypoint)

        if entry and node['prim'] not in ['or', 'pair', 'map', 'big_map', 'list', 'set', 'unit']:
            key = get_key(bin_path, entry)
            json_types[json_path] = 'dict' if key else 'list'
            bin_to_json[bin_path] = join(json_path, key or '0')
        else:
            bin_to_json[bin_path] = json_path

    parse_node()
    json_to_bin = {v: k for k, v in bin_to_json.items()}
    bin_types = {k: v['prim'] for k, v in metadata.items()}
    return bin_types, bin_to_json, json_types, json_to_bin


def parse_micheline(data, bin_to_json: dict, bin_types: dict, root='0'):
    json_values = dict()

    def is_map(sequence):
        return all(map(lambda x: isinstance(x, dict) and x.get('prim') == 'Elt', sequence))

    def parse_node(node, bin_path, params):
        if isinstance(node, dict):
            if node.get('prim') in ['Left', 'Some']:
                parse_node(node['args'][0], bin_path + '0', params)
            elif node.get('prim') == 'Right':
                parse_node(node['args'][0], bin_path + '1', params)
            elif node.get('prim') == 'Pair':
                for i, arg in enumerate(node['args']):
                    parse_node(arg, bin_path + str(i), params)
            elif node.get('prim') == 'Elt':
                assert False
            elif node.get('prim') == 'None':
                pass
            else:
                json_path = bin_to_json[bin_path].format(*params)
                json_values[json_path] = decode_literal(node, bin_types[bin_path])

        elif isinstance(node, list):
            if is_map(node):
                for elt in node:
                    key = next(iter(elt['args'][0].values()))
                    parse_node(elt['args'][1], bin_path + '1', params + [key])
            else:
                for i, arg in enumerate(node):
                    parse_node(arg, bin_path + '0', params + [i])
        else:
            raise ValueError(node, bin_path)

    parse_node(data, root, [])
    return json_values


def make_json(json_values: dict, json_types: dict):
    tree = {} if json_types['/'] == 'dict' else []

    for json_path, value in json_values.items():
        node = tree
        lpath = '/'

        for key in json_path.lstrip('/').split('/'):
            lpath = join(lpath, key)
            if key.isdigit():
                key = int(key)
            try:
                node = node[key]
            except (KeyError, IndexError):
                if isinstance(node, list):
                    node.extend([None] * (key - len(node) + 1))

                if lpath == json_path:
                    node[key] = value
                else:
                    node[key] = {} if json_types[lpath] == 'dict' else []
                    node = node[key]
    return tree


def parse_json(data, json_to_bin: dict, bin_types: dict, root='/'):
    bin_values = defaultdict(dict)

    def parse_node(node, json_path, index='0'):
        bin_path = json_to_bin[json_path]
        prim = bin_types[bin_path]

        if isinstance(node, dict):
            if prim in ['map', 'big_map']:
                bin_values[bin_path][index] = len(node)
                for i, (key, value) in enumerate(node.items()):
                    bin_values[bin_path + '0'][f'{index}:{i}'] = key
                    parse_node(value, join(json_path, '{}'), f'{index}:{i}')

            elif prim == 'or':
                assert len(node) == 1
                entry = next(iter(node))
                parse_node(node[entry], join(json_path, entry), index)

            elif prim == 'pair':
                for key, value in node.items():
                    parse_node(value, join(json_path, key), index)
            else:
                raise ValueError(node, json_path)

        elif isinstance(node, list):
            if prim in ['list', 'set']:
                bin_values[bin_path][index] = len(node)
                for i, value in enumerate(node):
                    parse_node(value, join(json_path, '{}'), f'{index}:{i}')

            elif prim == 'or':
                assert len(node) == 1
                parse_node(node[0], join(json_path, '0'), index)

            elif prim == 'pair':
                for i, value in enumerate(node):
                    parse_node(value, join(json_path, str(i)), index)
        else:
            if prim == 'or':
                print('enum', node)
            else:
                bin_values[bin_path][index] = node

    parse_node(data, root)
    return bin_values


def make_micheline(bin_values: dict, bin_types: dict, root='0'):

    def encode_node(bin_path, index='0'):
        prim = bin_types[bin_path]

        if prim == 'pair':
            return dict(
                prim='Pair',
                args=list(map(lambda x: encode_node(bin_path + x, index), '01'))
            )
        elif prim in ['map', 'big_map']:
            length = bin_values[bin_path][index]
            return [
                dict(
                    prim='Elt',
                    args=[encode_node(bin_path + '0', f'{index}:{i}'),
                          encode_node(bin_path + '1', f'{index}:{i}')]
                )
                for i in range(length)
            ]
        elif prim in ['set', 'list']:
            length = bin_values[bin_path][index]
            return [
                encode_node(bin_path + '0', f'{index}:{i}')
                for i in range(length)
            ]
        elif prim == 'or':
            for i in [0, 1]:
                try:
                    return dict(
                        prim={0: 'Left', 1: 'Right'}[i],
                        args=[encode_node(bin_path + str(i), index)]
                    )
                except KeyError:
                    continue
        elif prim == 'option':
            try:
                value = encode_node(bin_path + '0', index)
            except KeyError:
                return dict(prim='None')
            else:
                return dict(prim='Some', args=[value])

        return encode_literal(
            value=bin_values[bin_path][index],
            prim=prim
        )

    return encode_node(root)


def build_schema(code) -> Schema:
    return Schema(*build_maps(collapse_micheline(code)))


def decode_micheline(data, schema: Schema, root='0'):
    json_values = parse_micheline(data, schema.bin_to_json, data.bin_types, root)
    return make_json(json_values, schema.json_types)


def encode_micheline(data, schema: Schema, root='0'):
    json_root = schema.bin_to_json[root]
    bin_values = parse_json(data, schema.json_to_bin, schema.bin_types, json_root)
    return make_micheline(bin_values, schema.bin_types, root)
