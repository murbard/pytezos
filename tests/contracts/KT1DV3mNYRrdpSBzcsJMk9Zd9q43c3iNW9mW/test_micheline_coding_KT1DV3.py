from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1DV3(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/code_KT1DV3.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1DV3(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/storage_KT1DV3.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo5gaT(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_oo5gaT.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opPGAB(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_opPGAB.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ootr5F(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_ootr5F.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo64jf(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_oo64jf.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onk5NH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_onk5NH.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooc8Cj(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_ooc8Cj.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo9js3(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1DV3mNYRrdpSBzcsJMk9Zd9q43c3iNW9mW/parameter_oo9js3.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
