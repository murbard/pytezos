import os
import simplejson as json
from unittest import TestCase
from parameterized import parameterized

from pytezos.micheline.grammar import MichelineParser
from pytezos.micheline.schema import build_schema, decode_data, encode_data


def get_data(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path) as f:
        return f.read()


class TestMichelineParser(TestCase):

    def setUp(self):
        self.parser = MichelineParser()
        self.maxDiff = None

    @parameterized.expand([
        ('script/sample_0.tz', 'script/sample_0.json'),
        ('script/sample_1.tz', 'script/sample_1.json'),
        ('script/sample_2.tz', 'script/sample_2.json'),
    ])
    def test_parser(self, source_name, expected_name):
        source = get_data(source_name)
        res = self.parser.parse(source)
        expected = json.loads(get_data(expected_name))
        self.assertListEqual(expected, res)

    @parameterized.expand([
        ('storage/sample_0.json',),
        ('storage/sample_1.json',),
    ])
    def test_storage_parsing(self, source_name):
        script = json.loads(get_data(source_name))
        storage = next(s for s in script['code'] if s['prim'] == 'storage')
        schema = build_schema(storage)
        data = decode_data(script['storage'], schema)
        res = encode_data(data, schema)
        self.assertDictEqual(script['storage'], res)

    @parameterized.expand([
        ('parameter/code_0.json', 'parameter/parameters_0.json'),
    ])
    def test_parameter_parsing(self, code_name, parameters_name):
        code = json.loads(get_data(code_name))
        parameters = json.loads(get_data(parameters_name))
        schema = build_schema(code)
        data = decode_data(parameters, schema)
        res = encode_data(data, schema)
        self.assertDictEqual(parameters, res)
