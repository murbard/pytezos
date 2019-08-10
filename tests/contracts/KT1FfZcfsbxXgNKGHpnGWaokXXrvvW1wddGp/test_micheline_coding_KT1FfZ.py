from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1FfZ(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/code_KT1FfZ.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1FfZ(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/storage_KT1FfZ.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onz3sp(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_onz3sp.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op3k3r(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_op3k3r.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooWtpV(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_ooWtpV.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onhoAS(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_onhoAS.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooZzzH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_ooZzzH.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo9vEm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_oo9vEm.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opKR3R(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1FfZcfsbxXgNKGHpnGWaokXXrvvW1wddGp/parameter_opKR3R.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
