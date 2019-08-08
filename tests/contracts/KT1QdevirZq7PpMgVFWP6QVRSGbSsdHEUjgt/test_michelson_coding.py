from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTestKT1Qde(TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def test_michelson_parse_code_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/code_KT1Qde.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/code_KT1Qde.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_code_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/code_KT1Qde.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/code_KT1Qde.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_code_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/code_KT1Qde.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_storage_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/storage_KT1Qde.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/storage_KT1Qde.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_storage_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/storage_KT1Qde.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/storage_KT1Qde.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_storage_KT1Qde(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/storage_KT1Qde.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oo3Zu4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/parameter_oo3Zu4.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/parameter_oo3Zu4.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oo3Zu4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/parameter_oo3Zu4.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/parameter_oo3Zu4.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oo3Zu4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt/parameter_oo3Zu4.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
