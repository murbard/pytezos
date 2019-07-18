from functools import lru_cache

from pytezos.michelson.grammar import MichelsonParser
from pytezos.michelson.interface import build_schema, decode_data, encode_data, decode_schema

michelson_parser = MichelsonParser()
# Binary path for type map
BIG_MAP_KEY = '00'
BIG_MAP_VAL = '01'


def michelson_to_micheline(source):
    return michelson_parser.parse(source)


class Script:

    def __init__(self, code):
        """
        :param code: ['parameter': {}, 'storage': {}, 'code': {}]
        """
        self._code = code  # type: list

    def __repr__(self):
        return str(self._code)

    @classmethod
    def from_michelson(cls, source):
        return Script(michelson_to_micheline(source))

    @classmethod
    def from_tz_file(cls, path):
        with open(path) as f:
            return cls.from_michelson(f.read())

    def _get_section(self, section):
        return next(s for s in self._code if s['prim'] == section)

    @lru_cache(maxsize=None)
    def _get_schema(self, section):
        return build_schema(self._get_section(section))

    def storage_schema(self):
        return decode_schema(self._get_schema('storage'))

    def parameter_schema(self):
        return decode_schema(self._get_schema('parameter'))

    def storage_decode(self, expr, annotations=True, literals=True):
        """
        :param expr: Micheline expression
        :param annotations: Try to produce named entities using annotations (true by default)
        :param literals: Try to decode known types (true by default)
        :return: object
        """
        return decode_data(
            data=expr,
            schema=self._get_schema('storage'),
            annotations=annotations,
            literals=literals
        )

    def storage_encode(self, data):
        return encode_data(
            data=data,
            schema=self._get_schema('storage')
        )

    def parameters_decode(self, expr, annotations=True, literals=True):
        """
        :param expr: Micheline expression
        :param annotations: Try to produce named entities using annotations (true by default)
        :param literals: Try to decode known types (true by default)
        :return: object
        """
        return decode_data(
            data=expr,
            schema=self._get_schema('parameter'),
            annotations=annotations,
            literals=literals
        )

    def parameters_encode(self, data):
        return encode_data(
            data=data,
            schema=self._get_schema('parameter')
        )

    def big_map_query(self, key):
        schema = self._get_schema('storage')
        return dict(
            key=encode_data(key, schema, root=BIG_MAP_KEY),
            type=schema.type_map[BIG_MAP_KEY]
        )

    def big_map_decode(self, val):
        schema = self._get_schema('storage')
        return decode_data(val, schema, root=BIG_MAP_VAL)

    def big_map_diff_decode(self, diff):
        schema = self._get_schema('storage')
        return {
            decode_data(item['key'], schema, root=BIG_MAP_KEY):
                decode_data(item['value'], schema, root=BIG_MAP_VAL)
            for item in diff
        }
