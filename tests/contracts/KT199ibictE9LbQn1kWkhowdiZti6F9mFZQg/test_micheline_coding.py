from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT199i(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/code_KT199i.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT199i(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/storage_KT199i.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oomgeZ(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/parameter_oomgeZ.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oogdua(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/parameter_oogdua.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oopFEw(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/parameter_oopFEw.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oof2Jx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/parameter_oof2Jx.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oogbBk(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT199ibictE9LbQn1kWkhowdiZti6F9mFZQg/parameter_oogbBk.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
