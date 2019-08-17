from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1NwV(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/code_KT1NwV.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1NwV(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/storage_KT1NwV.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oofBMc(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_oofBMc.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onrPzn(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_onrPzn.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo7g8y(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_oo7g8y.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opWEgz(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_opWEgz.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oogZVX(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_oogZVX.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opLEjp(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_opLEjp.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo2ZBR(self):
        expected = get_data(
            path='contracts/KT1NwVhTTfmKSYnxecwb6isyJUK5LvuYYDfB/parameter_oo2ZBR.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)