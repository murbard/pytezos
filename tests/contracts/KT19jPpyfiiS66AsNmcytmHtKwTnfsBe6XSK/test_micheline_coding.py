from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT19jP(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op6Jjx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onrsfd(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onnVBH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opQjjr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooaW9j(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onnBLb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooJ3VU(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op8Bbm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oohuCM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooMXxF(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
