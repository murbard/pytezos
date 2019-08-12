michelson_coding_test_case = """from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTest{case}(TestCase):
    
    def setUp(self):
        self.maxDiff = None
"""


test_michelson_parse = """
    def test_michelson_parse_{case}(self):
        expected = get_data(
            path='{json_path}')
        actual = michelson_to_micheline(get_data(
            path='{tz_path}'))
        self.assertEqual(expected, actual)
"""


test_michelson_format = """
    def test_michelson_format_{case}(self):
        expected = get_data(
            path='{tz_path}')
        actual = micheline_to_michelson(get_data(
            path='{json_path}'), 
            inline=True)
        self.assertEqual(expected, actual)
"""


test_michelson_inverse = """
    def test_michelson_inverse_{case}(self):
        expected = get_data(
            path='{json_path}')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
"""


micheline_coding_test_case = """from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import build_schema, encode_micheline, decode_micheline


class MichelineCodingTest{case}(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        code = get_data(
            path='{json_path}')
        cls.schema = dict(
            parameter=build_schema(code[0]),
            storage=build_schema(code[1])
        )
"""


test_micheline_inverse = """
    def test_micheline_inverse_{case}(self):
        expected = get_data(
            path='{json_path}')
        decoded = decode_micheline(expected, self.schema['{section}'])
        actual = encode_micheline(decoded, self.schema['{section}'])
        self.assertEqual(expected, actual)
"""


operation_forging_test_case = """from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTest{case}(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_{case}(self):
        expected = get_data(
            path='{hex_path}')
        actual = forge_operation_group(get_data(
            path='{json_path}'))
        self.assertEqual(expected, actual)
"""
