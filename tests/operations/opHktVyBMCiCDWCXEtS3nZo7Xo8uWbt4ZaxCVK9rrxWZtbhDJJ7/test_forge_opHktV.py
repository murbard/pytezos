from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopHktV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opHktV(self):
        expected = get_data(
            path='operations/opHktVyBMCiCDWCXEtS3nZo7Xo8uWbt4ZaxCVK9rrxWZtbhDJJ7/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opHktVyBMCiCDWCXEtS3nZo7Xo8uWbt4ZaxCVK9rrxWZtbhDJJ7/unsigned.json'))
        self.assertEqual(expected, actual)
