from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1At3(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/code_KT1At3.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1At3(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/storage_KT1At3.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oozfkT(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_oozfkT.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo2UMR(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_oo2UMR.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onwvUM(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_onwvUM.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opGhNz(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_opGhNz.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oowDU8(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_oowDU8.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onpSQy(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_onpSQy.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oopBY6(self):
        expected = get_data(
            path='contracts/KT1At3oM7k94ccMmFCqjAZy42QyaDh2uNqhD/parameter_oopBY6.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
