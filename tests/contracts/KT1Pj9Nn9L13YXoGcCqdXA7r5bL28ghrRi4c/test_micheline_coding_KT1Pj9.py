from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1Pj9(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT1Pj9Nn9L13YXoGcCqdXA7r5bL28ghrRi4c/code_KT1Pj9.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1Pj9(self):
        expected = get_data(
            path='contracts/KT1Pj9Nn9L13YXoGcCqdXA7r5bL28ghrRi4c/storage_KT1Pj9.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)
