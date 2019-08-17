from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1Mqv(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT1MqvzsEPoZnbacH18uztqvQdG8x8nKAgFi/code_KT1Mqv.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1Mqv(self):
        expected = get_data(
            path='contracts/KT1MqvzsEPoZnbacH18uztqvQdG8x8nKAgFi/storage_KT1Mqv.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)
