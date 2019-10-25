from functools import lru_cache
from os.path import basename, exists, expanduser

from pytezos.tools.docstring import get_class_docstring, InlineDocstring
from pytezos.michelson.docstring import generate_docstring
from pytezos.michelson.micheline import encode_literal, decode_literal, make_default, michelson_to_micheline
from pytezos.michelson.formatter import micheline_to_michelson
from pytezos.michelson.converter import build_schema, decode_micheline, encode_micheline


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

    def _get_entry_root(self, entrypoint):
        if entrypoint == 'root':
            return '0'
        else:
            return self.schema.json_to_bin[f'/{entrypoint}']

    def decode(self, data):
        """
        Convert Micheline data into Python object using internal schema.
        :param data: Micheline expression or Michelson string or {entrypoint: "string", value: "expression"}
        :return: object
        """
        if isinstance(data, dict) \
                and set(data.keys()) == {'entrypoint', 'value'} \
                and data['entrypoint'] != 'root':
            res = decode_micheline(data, self.schema, root=self._get_entry_root(data['entrypoint']))
            return {data['entrypoint']: res}
        else:
            if isinstance(data, str):
                data = michelson_to_micheline(data)

            return decode_micheline(data, self.schema)

    def encode(self, data):
        """
        Convert Python object to Micheline expression using internal schema.
        :param data: Python object
        :return: object
        """
        if isinstance(data, dict) and len(data) == 1:
            entrypoint = next(iter(data))
            value = encode_micheline(data[entrypoint], self.schema, root=self._get_entry_root(entrypoint))
        else:
            entrypoint = 'root'
            value = encode_micheline(data, self.schema)

        return dict(entrypoint=entrypoint, value=value)

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
        if diff:
            key_prim, value_root = self._locate_big_map(big_map_path)
            return {
                decode_literal(item['key'], key_prim):
                    decode_micheline(item['value'], self.schema, root=value_root) if item.get('value') else None
                for item in diff
                if item.get('action') != 'alloc'
            }
        else:
            return {}

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
        with open(expanduser(path)) as f:
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

    def script(self, storage=None, original=True):
        """
        Generate script for contract origination
        :param storage: Python object, leave None to generate empty
        :param original: Keep the original code (initialized), which is default.
        Otherwise factory-specific changes may applied, e.g. different annotations
        :return: {"code": $Micheline, "storage": $Micheline}
        """
        if storage is None:
            storage = self.storage.default()
        else:
            storage = self.storage.encode(storage)

        if original:
            code = self.code
        else:
            code = [
                self.parameter.code,
                self.storage.code,
                self.code[-1]
            ]

        return {
            "code": code,
            "storage": storage
        }
