from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohkvm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohkvm(self):
        expected = get_data(
            path='operations/oohkvmL86qKZGH2hEm2k6xTMNzn4erwCU24zvP8zUkzYXqoJqH8/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohkvmL86qKZGH2hEm2k6xTMNzn4erwCU24zvP8zUkzYXqoJqH8/unsigned.json'))
        self.assertEqual(expected, actual)
