from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1T6C(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T6CDRQLRiFU5dszBZWWQwQc8aCbfwX3Mg/code_KT1T6C.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1T6C(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T6CDRQLRiFU5dszBZWWQwQc8aCbfwX3Mg/storage_KT1T6C.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooQKSw(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T6CDRQLRiFU5dszBZWWQwQc8aCbfwX3Mg/parameter_ooQKSw.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
