from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1Myq(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/code_KT1Myq.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1Myq(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/storage_KT1Myq.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooZMtN(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_ooZMtN.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooGGqi(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_ooGGqi.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opYTCv(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_opYTCv.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op1CjT(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_op1CjT.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onyJat(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_onyJat.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooPQUi(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_ooPQUi.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op1KRF(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Myqcyxp8MNgdB1aAhMpBApZHgVJ634nhm/parameter_op1KRF.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
