from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1Jyf(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Jyf1eYy988fGDwmv1EybaaqvmpSH4B9us/code_KT1Jyf.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1Jyf(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Jyf1eYy988fGDwmv1EybaaqvmpSH4B9us/storage_KT1Jyf.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)
