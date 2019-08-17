from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo9A51(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo9A51(self):
        expected = get_data(
            path='operations/oo9A51ehy3euCgBcMAeEFxSmUaGsqCTUnd5jdMrhY42RPbG8HnQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo9A51ehy3euCgBcMAeEFxSmUaGsqCTUnd5jdMrhY42RPbG8HnQ/unsigned.json'))
        self.assertEqual(expected, actual)
