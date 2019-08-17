from functools import lru_cache
from os.path import basename, exists, expanduser

from pytezos.tools.docstring import get_class_docstring, InlineDocstring
from pytezos.michelson.coding import build_schema, decode_micheline, encode_micheline, Schema, \
    encode_literal, decode_literal, michelson_to_micheline, make_default, micheline_to_michelson

core_types = ['string', 'int', 'bool']
domain_types = {
    'nat': 'int  /* Natural number */',
    'unit': 'None /* Void */',
    'bytes': 'string  /* Hex string */ ||\n\tbytes  /* Python byte string */',
    'timestamp': 'int  /* Unix time in seconds */ ||\n\tstring  /* Formatted datetime `%Y-%m-%dT%H:%M:%SZ` */',
    'mutez': 'int  /* Amount in `utz` (10^-6) */ ||\n\tDecimal  /* Amount in `tz` */',
    'contract': 'string  /* Base58 encoded `KT` address */',
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
            if bin_type == 'big_map':
                res += '  /* big_map */'

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

            if node['prim'] in ['contract', 'lambda']:
                parameter = schema.metadata[bin_path]['parameter']
                res = f'{res} ({parameter})'

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


class ContractParameter(metaclass=InlineDocstring):

    def __init__(self, section):
        self.code = section
        self.schema = build_schema(section)
        self.__doc__ = generate_docstring(self.schema, 'parameter')

    def __repr__(self):
        res = [
            super(ContractParameter, self).__repr__(),
            f'\n{self.__doc__}',
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def decode(self, data):
        """
        Convert Micheline data into Python object using internal schema.
        :param data: Micheline expression or Michelson string
        :return: object
        """
        if isinstance(data, str):
            data = michelson_to_micheline(data)
        return decode_micheline(data, self.schema)

    def encode(self, data):
        """
        Convert Python object to Micheline expression using internal schema.
        :param data: Python object
        :return: object
        """
        return encode_micheline(data, self.schema)

    def entries(self, default='call'):
        """
        Get list of entrypoints: names and docstrings.
        :param default: Name of the single entrypoint
        :return: list[tuple]
        """
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


class ContractStorage(metaclass=InlineDocstring):

    def __init__(self, section):
        self.code = section
        self.schema = build_schema(section)
        self.__doc__ = generate_docstring(self.schema, 'storage')

    def __repr__(self):
        res = [
            super(ContractStorage, self).__repr__(),
            f'\n{self.__doc__}',
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def decode(self, data):
        """
        Convert Micheline data into Python object using internal schema.
        :param data: Micheline expression or Michelson string
        :return: object
        """
        if isinstance(data, str):
            data = michelson_to_micheline(data)
        return decode_micheline(data, self.schema)

    def encode(self, data):
        """
        Convert Python object to Micheline expression using internal schema.
        :param data: Python object
        :return: object
        """
        return encode_micheline(data, self.schema)

    def default(self, root='0'):
        """
        Try to generate empty storage, returns Micheline expression
        :param root: binary path to start from, default is '0'
        :return: object
        """
        return make_default(self.schema.bin_types, root)

    def _locate_big_map(self, big_map_path=None):
        if big_map_path is None:
            # Default Big Map location (prior to Babylon https://blog.nomadic-labs.com/michelson-updates-in-005.html)
            return self.schema.bin_types['000'], '001'
        else:
            bin_path = self.schema.json_to_bin[big_map_path]
            return self.schema.bin_types[bin_path + '0'], bin_path + '1'

    def big_map_query(self, key, big_map_path=None):
        """
        Construct a query for big_map_get request
        :param key: BigMap key, string, int, or hex-string
        :param big_map_path: Json path to BigMap, leave None to use default
        (since Babylon you can have more than one BigMap at arbitrary position)
        :return: dict
        """
        # TODO: convert to big_map id (integer)
        key_prim, _ = self._locate_big_map(big_map_path)
        return dict(
            key=encode_literal(key, key_prim),
            type={'prim': key_prim}
        )

    def big_map_decode(self, value, big_map_path=None):
        """
        Convert big_map_get result into a Python object
        :param value: Micheline expression for a BigMap entry
        :param big_map_path: Json path to BigMap, leave None to use default
        (since Babylon you can have more than one BigMap at arbitrary position)
        :return: object
        """
        _, value_root = self._locate_big_map(big_map_path)
        return decode_micheline(value, self.schema, root=value_root)

    def big_map_diff_decode(self, diff: list, big_map_path=None) -> dict:
        """
        Convert big_map_diff from operation_result section into Python objects
        :param diff: [{"key": $micheline, "value": $micheline}, ...]
        :param big_map_path: Json path to BigMap, leave None to use default
        (since Babylon you can have more than one BigMap at arbitrary position)
        :return: dict
        """
        key_prim, value_root = self._locate_big_map(big_map_path)
        return {
            decode_literal(item['key'], key_prim):
                decode_micheline(item['value'], self.schema, root=value_root) if item.get('value') else None
            for item in diff
        }

    def big_map_diff_encode(self, big_map: dict, big_map_path=None):
        """
        Convert Python representation of BigMap (dict) into big_map_diff
        :param big_map: { $key: $micheline, ... }
        :param big_map_path: Json path to BigMap, leave None to use default
        (since Babylon you can have more than one BigMap at arbitrary position)
        :return: [{"key": $micheline, "value": $micheline}, ... ]
        """
        key_prim, value_root = self._locate_big_map(big_map_path)

        def make_item(x):
            key = encode_literal(x[0], key_prim, binary=True)
            if x[1] is not None:
                value = encode_micheline(x[1], self.schema, root=value_root, binary=True)
            else:
                value = None
            return {"key": key, "value": value}

        return list(map(make_item, big_map.items()))


class Contract(metaclass=InlineDocstring):

    def __init__(self, code: list):
        self.code = code

    def __repr__(self):
        res = [
            super(Contract, self).__repr__(),
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def __str__(self):
        return self.text

    @property
    @lru_cache(maxsize=None)
    def parameter(self) -> ContractParameter:
        return ContractParameter(self.code[0])

    @property
    @lru_cache(maxsize=None)
    def storage(self) -> ContractStorage:
        return ContractStorage(self.code[1])

    @property
    @lru_cache(maxsize=None)
    def text(self):
        return micheline_to_michelson(self.code)

    @classmethod
    def from_micheline(cls, code):
        """
        Create contract from micheline expression.
        :param code: [{'prim': 'parameter'}, {'prim': 'storage'}, {'prim': 'code'}]
        :return: Contract
        """
        return cls(code)

    @classmethod
    def from_michelson(cls, text):
        """
        Create contract from michelson source code.
        :param text:
        :return: Contract
        """
        return cls(michelson_to_micheline(text))

    @classmethod
    def from_file(cls, path):
        """
        Create contract from michelson source code stored in file.
        :param path: Path to the `.tz` file
        :return: Contract
        """
        with open(path) as f:
            return cls.from_michelson(f.read())

    def save_file(self, path, overwrite=False):
        """
        Save Michelson code to file
        :param path: Output path
        :param overwrite: Default is False
        """
        path = expanduser(path)
        if exists(path) and not overwrite:
            raise FileExistsError(path)

        with open(path, 'w+') as f:
            f.write(self.text)

    def script(self, storage=None):
        """
        Generate script for contract origination
        :param storage: Python object, leave None to generate empty
        :return: {"code": $Micheline, "storage": $Micheline}
        """
        if storage is None:
            storage = self.storage.default()
        else:
            storage = self.storage.encode(storage)

        return {
            "code": self.code,
            "storage": storage
        }
