from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1Rvo(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/code_KT1Rvo.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1Rvo(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/storage_KT1Rvo.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onfSmx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_onfSmx.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oowFNb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_oowFNb.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opCeKS(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_opCeKS.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooGbyw(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_ooGbyw.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op7xJA(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_op7xJA.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onzWYC(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_onzWYC.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooUiCY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1RvoWEU4MfDBrTbJh4JEAdh3giXtjxkR7k/parameter_ooUiCY.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
