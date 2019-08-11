from functools import lru_cache
from os.path import basename

from pytezos.michelson.coding import build_schema, decode_micheline, encode_micheline, Schema, \
    encode_literal, decode_literal, michelson_to_micheline, make_default, micheline_to_michelson

core_types = ['string', 'int', 'bool']
domain_types = {
    'nat': 'int  /* Natural number */',
    'unit': 'None /* Void */',
    'bytes': 'string  /* Hex string */ ||\n\tbytes  /* Python byte string */',
    'timestamp': 'int  /* Unix time in seconds */ ||\n\tstring  /* Formatted datetime `%Y-%m-%dT%H:%M:%SZ` */',
    'mutez': 'int  /* Amount in `utz` (10^-6) */ ||\n\tDecimal  /* Amount in `tz` */',
    'contract': 'string  /* Base58 encoded implicit `KT` address */',
    'address': 'string  /* Base58 encoded `tz` or `KT` address */',
    'key': 'string  /* Base58 encoded public key */',
    'key_hash': 'string  /* Base58 encoded public key hash */',
    'signature': 'string  /* Base58 encoded signature */',
    'lambda': 'string  /* Michelson source code */'
}


def generate_docstring(schema: Schema, title, root='0'):
    docstring = list()
    known_types = set()

    def get_node(bin_path):
        return schema.metadata[bin_path]

    def get_name(bin_path):
        return basename(schema.bin_to_json[bin_path])

    def get_type(bin_path):
        default = get_name(bin_path[:-1]) + '_item'
        return schema.metadata[bin_path].get('typename', default)

    def get_comment(bin_path):
        node = schema.metadata[bin_path]
        return node.get('typename', node.get('fieldname'))

    def is_optional(bin_path):
        return len(bin_path) > 1 and schema.bin_types[bin_path[:-1]] == 'option'

    def decode_node(bin_path, is_element=False, is_entry=False):
        node = get_node(bin_path)
        bin_type = schema.bin_types[bin_path]

        def get_struct_name():
            if bin_path == root:
                struct_name = title
            elif is_element:
                struct_name = get_type(bin_path)
            else:
                struct_name = get_name(bin_path)
            return f'${struct_name}'

        if bin_type == 'router':
            entries = {get_name(x): decode_node(x, is_entry=True) for x in node['args']}
            doc = ' || \n\t'.join(map(lambda x: '{ ' + f'"{x[0]}": {x[1]}' + ' }', entries.items()))
            res = get_struct_name()
            docstring.insert(0, f'{res}:\n\t{doc}\n')
            return res

        elif bin_type == 'enum':
            res = ' || '.join(map(lambda x: f'"{get_name(x)}"', node['args']))

        elif bin_type == 'namedtuple':
            items = map(lambda x: (get_name(x), decode_node(x)), node['args'])
            lines = map(lambda x: f'  "{x[0]}": {x[1]}', items)
            doc = '\t{\n\t' + ',\n\t'.join(lines) + '\n\t}'
            res = get_struct_name()
            docstring.insert(0, f'{res}:\n{doc}\n')
            return res

        elif bin_type == 'tuple':
            values = map(decode_node, node['args'])
            res = f'[ {" , ".join(values)} ]'

        elif bin_type in {'set', 'list'}:
            value = decode_node(node['args'][0], is_element=True)
            res = f'[ {value} , ... ]'

        elif bin_type in {'map', 'big_map'}:
            item = (decode_node(node['args'][0]), decode_node(node['args'][1], is_element=True))
            res = '{ ' + f'{item[0]} : {item[1]} , ...' + ' }'

        else:
            res = node['prim']
            if res not in core_types:
                res = f'${res}'

            if is_optional(bin_path):
                res = f'{res}?'

            if is_entry:
                comment = get_comment(bin_path)
                if comment:
                    res = f'{res}  /* {comment} */'

            if node['prim'] not in core_types:
                if bin_path == root:
                    res = domain_types[node["prim"]]
                else:
                    known_types.add(node['prim'])

        if bin_path == root:
            docstring.insert(0, f'${title}:\n\t{res}\n')

        return res

    decode_node(root)

    for prim in known_types:
        docstring.append(f'${prim}:\n\t{domain_types[prim]}\n')

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

        def make_docs(bin_path):
            if self.schema.bin_types[bin_path] in ['namedtuple', 'router']:
                title = 'kwargs'
            else:
                title = 'args'
            return generate_docstring(self.schema, title, bin_path)

        return list(map(lambda x: (x[0], make_docs(x[1])), entries))


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

    def default(self, root='0'):
        return make_default(self.schema.bin_types, root)

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
        self.parameter = ContractParameter(code[0])
        self.storage = ContractStorage(code[1])
        self.code = code
        self.text = micheline_to_michelson(code)

    def __repr__(self):
        return self.text

    @classmethod
    def from_micheline(cls, code):
        """
        :param code: [{'prim': 'parameter'}, {'prim': 'storage'}, {'prim': 'code'}]
        """
        return cls(code)

    @classmethod
    def from_michelson(cls, text):
        """

        :param text:
        :return:
        """
        return cls(michelson_to_micheline(text))

    @classmethod
    def from_file(cls, path):
        """

        :param path:
        :return:
        """
        with open(path) as f:
            return cls.from_michelson(f.read())
