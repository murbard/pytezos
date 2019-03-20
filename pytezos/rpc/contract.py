from pytezos.rpc.node import RpcQuery
from pytezos.michelson.grammar import MichelsonParser
from pytezos.michelson.schema import parse_schema, decode_data, encode_data

michelson_parser = MichelsonParser()


class Contract(RpcQuery):

    def __init__(self, code=None, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)
        self._code = code

    def _get_code(self):
        if self._code:
            return self._code
        return self.get('script')['code']

    def _get_section(self, section):
        code = self._get_code()
        return next(s for s in code if s['prim'] == section)

    def _get_schema(self, section):
        return parse_schema(self._get_section(section))

    @classmethod
    def from_code(cls, code):
        return Contract(code=code)

    @classmethod
    def from_string(cls, text):
        code = michelson_parser.parse(text)
        return cls.from_code(code)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_string(f.read())

    def decode_storage(self, data=None, annotations=True, literals=True):
        if data in None:
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
