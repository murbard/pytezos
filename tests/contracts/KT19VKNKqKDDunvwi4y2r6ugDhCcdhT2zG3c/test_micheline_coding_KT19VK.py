from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTestKT19VK(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/code_KT19VK.json')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )

    def test_micheline_inverse_storage_KT19VK(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/storage_KT19VK.json')
        decoded = decode_micheline(expected, self.schema['storage'])
        actual = encode_micheline(decoded, self.schema['storage'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onr6zv(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_onr6zv.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_onzZ9j(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_onzZ9j.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_ooCm5y(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_ooCm5y.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oozEnM(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_oozEnM.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo9VWb(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_oo9VWb.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_opP9oc(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_opP9oc.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)

    def test_micheline_inverse_parameter_oo73cY(self):
        expected = get_data(
            path='contracts/KT19VKNKqKDDunvwi4y2r6ugDhCcdhT2zG3c/parameter_oo73cY.json')
        decoded = decode_micheline(expected, self.schema['parameter'])
        actual = encode_micheline(decoded, self.schema['parameter'])
        self.assertEqual(expected, actual)
