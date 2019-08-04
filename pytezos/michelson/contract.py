from functools import lru_cache
from os.path import basename, join

from pytezos.michelson import michelson_to_micheline
from pytezos.michelson.coding import build_schema, decode_micheline, encode_micheline, Schema, \
    encode_literal, decode_literal

core_types = ['string', 'int', 'nat', 'bool']
domain_types = {
    'unit': 'No arguments, set to `None` or any empty container ({}, [], "")',
    'bytes': 'Hex string (string) or Python byte string (bytes)',
    'timestamp': 'Unix time in millis (int), or formatted datetime `%Y-%m-%dT%H:%M:%SZ` (string)',
    'mutez': 'Amount in `utz` (int) or in `tz` (Decimal)',
    'contract': 'Base58 encoded implicit `KT` address (string)',
    'address': 'Base58 encoded `tz` or `KT` address (string)',
    'key': 'Base58 encoded public key (string)',
    'key_hash': 'Base58 encoded public key hash (string)',
    'signature': 'Base58 encoded signature (string)',
    'lambda': 'Michelson source code (string)'
}


def generate_docstring(schema: Schema, title, root='0'):
    docstring = list()
    known_types = set()

    def get_node(bin_path):
        return schema.metadata[bin_path]

    def get_name(bin_path):
        return basename(schema.bin_to_json[bin_path])

    def is_optional(bin_path):
        return len(bin_path) > 1 and schema.bin_types[bin_path[:-1]] == 'option'

    def decode_node(bin_path, is_element=False):
        node = get_node(bin_path)

        def get_struct_name():
            if bin_path == root:
                struct_name = title
            elif is_element:
                struct_name = get_name(bin_path[:-1]) + '_item'
            else:
                struct_name = get_name(bin_path)
            return f'${struct_name}'

        if node['prim'] == 'or':
            entries = {get_name(x): decode_node(x) for x in node['args']}
            doc = ' || \n\t'.join(map(lambda x: '{ ' + f'"{x[0]}": {x[1]}' + ' }', entries.items()))
            res = get_struct_name()
            docstring.insert(0, f'{res}:\n\t{doc}\n')
            return res

        elif node['prim'] == 'pair':
            items = list(map(lambda x: (get_name(x), decode_node(x)), node['args']))
            names, values = zip(*items)
            if all(map(lambda x: x.isdigit(), names)):
                res = f'[ {" , ".join(values)} ]'
            else:
                lines = map(lambda x: f'  "{x[0]}": {x[1]}' if isinstance(x, tuple) else x, items)
                doc = '\t{\n\t' + ',\n\t'.join(lines) + '\n\t}'
                res = get_struct_name()
                docstring.insert(0, f'{res}:\n{doc}\n')
                return res

        elif node['prim'] in ['set', 'list']:
            value = decode_node(node['args'][0], is_element=True)
            res = f'[ {value} , ... ]'

        elif node['prim'] in {'map', 'big_map'}:
            item = (decode_node(node['args'][0]), decode_node(node['args'][1], is_element=True))
            res = '{ ' + f'{item[0]} : {item[1]} , ...' + ' }'

        else:
            res = node['prim']
            if res not in core_types:
                res = f'${res}'
            if is_optional(bin_path):
                res = f'{res}?'
            if node['prim'] not in core_types:
                if bin_path == root:
                    res = f'{res}  /* {domain_types[node["prim"]]} */'
                else:
                    known_types.add(node['prim'])

        if bin_path == root:
            docstring.insert(0, f'${title}:\n\t{res}\n')

        return res

    decode_node(root)

    for prim in known_types:
        docstring.append(f'${prim}:\n\t/* {domain_types[prim]} */\n')

    return '\n'.join(docstring)


class ContractParameter:

    def __init__(self, section):
        self.code = section
        self.schema = build_schema(section)

    @lru_cache(maxsize=None)
    def __repr__(self):
        return generate_docstring(self.schema, 'parameter')

    def decode(self, data):
        if isinstance(data, str):
            data = michelson_to_micheline(data)
        return decode_micheline(data, self.schema)

    def encode(self, data):
        return encode_micheline(data, self.schema)

    def entries(self, default='call'):
        if self.schema.metadata['0']['prim'] == 'or':
            entries = [
                (basename(self.schema.bin_to_json[bin_path]), bin_path)
                for bin_path in self.schema.metadata['0']['args']
            ]
        else:
            entries = [(default, '0')]

        return list(map(lambda x: (x[0], generate_docstring(self.schema, 'args', x[1])), entries))


class ContractStorage:

    def __init__(self, section):
        self.code = section
        self.schema = build_schema(section)

    @lru_cache(maxsize=None)
    def __repr__(self):
        return generate_docstring(self.schema, 'storage')

    def decode(self, data):
        if isinstance(data, str):
            data = michelson_to_micheline(data)
        return decode_micheline(data, self.schema)

    def encode(self, data):
        return encode_micheline(data, self.schema)

    def _locate_big_map(self, big_map_path=None):
        if big_map_path is None:
            # Default Big Map location (prior to Babylon https://blog.nomadic-labs.com/michelson-updates-in-005.html)
            return self.schema.bin_types['000'], '001'
        else:
            bin_path = self.schema['storage'].json_to_bin[big_map_path]
            return self.schema.bin_types[bin_path + '0'], bin_path + '1'

    def big_map_query(self, key, big_map_path=None):
        # TODO: convert to big_map id (integer)
        key_prim, _ = self._locate_big_map(big_map_path)
        return dict(
            key=encode_literal(key, key_prim),
            type={'prim': key_prim}
        )

    def big_map_decode(self, value, big_map_path=None):
        _, value_root = self._locate_big_map(big_map_path)
        return decode_micheline(value, self.schema, root=value_root)

    def big_map_diff_decode(self, diff: list, big_map_path=None):
        key_prim, value_root = self._locate_big_map(big_map_path)
        return {
            decode_literal(item['key'], key_prim):
                decode_micheline(item['value'], self.schema, root=value_root)
            for item in diff
        }


class Contract:

    def __init__(self, code: list):
        """
        :param code: [{'prim': 'parameter'}, {'prim': 'storage'}, {'prim': 'code'}]
        """
        self.parameter = ContractParameter(code[0])
        self.storage = ContractStorage(code[1])
        self.code = code

    @classmethod
    def from_micheline(cls, code):
        return cls(code)

    @classmethod
    def from_michelson(cls, source):
        return cls(michelson_to_micheline(source))

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_michelson(f.read())
