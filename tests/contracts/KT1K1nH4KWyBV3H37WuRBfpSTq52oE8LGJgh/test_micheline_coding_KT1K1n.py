from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1K1n(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1K1nH4KWyBV3H37WuRBfpSTq52oE8LGJgh/code_KT1K1n.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1K1n(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1K1nH4KWyBV3H37WuRBfpSTq52oE8LGJgh/storage_KT1K1n.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)
