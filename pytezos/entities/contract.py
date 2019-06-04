from functools import lru_cache

from pytezos.rpc.node import RpcQuery
from pytezos.micheline.grammar import MichelineParser
from pytezos.micheline.schema import build_schema, decode_data, encode_data, decode_schema

micheline_parser = MichelineParser()


class Contract(RpcQuery):

    def __init__(self, code=None, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)
        self._code = code

    def __repr__(self):
        if self._code:
            return str(self._code)
        return super(Contract, self).__repr__()

    def get_code(self):
        if self._code:
            return self._code
        return self.get('script')['code']

    def get_section(self, section):
        code = self.get_code()
        return next(s for s in code if s['prim'] == section)

    @lru_cache(maxsize=None)
    def _get_schema(self, section):
        return build_schema(self.get_section(section))

    def _get_big_map_schema(self):
        schema = self._get_schema('storage')
        root = next(k for k, v in schema.type_map.items() if v['prim'] == 'big_map')
        key_path, val_path = root + '0', root + '1'
        return schema, key_path, val_path

    @classmethod
    def from_code(cls, code):
        return Contract(code=code)

    @classmethod
    def from_string(cls, text):
        code = micheline_parser.parse(text)
        return cls.from_code(code)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_string(f.read())

    def decode_storage(self, data=None, annotations=True, literals=True):
        if data is None:
            data = self.get('script')['storage']

        return decode_data(
            data=data,
            schema=self._get_schema('storage'),
            annotations=annotations,
            literals=literals
        )

    def encode_storage(self, data):
        return encode_data(
            data=data,
            schema=self._get_schema('storage')
        )

    def decode_parameters(self, data, annotations=True, literals=True):
        return decode_data(
            data=data,
            schema=self._get_schema('parameter'),
            annotations=annotations,
            literals=literals
        )

    def encode_parameters(self, data):
        return encode_data(
            data=data,
            schema=self._get_schema('parameter')
        )

    def storage_schema(self):
        return decode_schema(self._get_schema('storage'))

    def parameter_schema(self):
        return decode_schema(self._get_schema('parameter'))

    def big_map_get(self, key):
        schema, key_path, val_path = self._get_big_map_schema()
        query = dict(
            key=encode_data(key, schema, root=key_path),
            type=schema.type_map[key_path]
        )
        value = self._node.post(f'{self._path}/big_map_get', json=query)
        return decode_data(value, schema, root=val_path)

    def big_map_diff_decode(self, data):
        schema, key_path, val_path = self._get_big_map_schema()
        return {
            decode_data(item['key'], schema, root=key_path):
                decode_data(item['value'], schema, root=val_path)
            for item in data
        }
