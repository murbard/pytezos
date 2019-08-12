from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1NAn(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/code_KT1NAn.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1NAn(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/storage_KT1NAn.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooJRq1(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/parameter_ooJRq1.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opYqMC(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/parameter_opYqMC.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opKWiC(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/parameter_opKWiC.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooZs8c(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/parameter_ooZs8c.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opMiJz(self):
        expected = get_data(
            path='contracts/KT1NAnXMYFDbABvejVCE7TYqMQPr1cUmP25U/parameter_opMiJz.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
