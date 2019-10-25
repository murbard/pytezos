from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo1SMJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo1SMJ(self):
        expected = get_data(
            path='operations/oo1SMJXUQ99TQwxj2fASQYu4YPhtCgZrNuDyLKfN6iPpFeCzNep/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo1SMJXUQ99TQwxj2fASQYu4YPhtCgZrNuDyLKfN6iPpFeCzNep/unsigned.json'))
        self.assertEqual(expected, actual)
