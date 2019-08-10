from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT1TEy(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/code_KT1TEy.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT1TEy(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/storage_KT1TEy.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooSJeE(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_ooSJeE.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opKSUG(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_opKSUG.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ootApt(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_ootApt.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo7dXA(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_oo7dXA.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opJMM9(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_opJMM9.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_op6KiD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_op6KiD.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onkFnb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1TEyRcaJi39jgj4Uuz7VD6Jmn6CDDADv4x/parameter_onkFnb.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
