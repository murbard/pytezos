from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooeB8V(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooeB8V(self):
        expected = get_data(
            path='operations/ooeB8VdKX6BdXwAAw1o7FLkPGT5XNrm3X6kvMUyicJE1sQkNk9V/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooeB8VdKX6BdXwAAw1o7FLkPGT5XNrm3X6kvMUyicJE1sQkNk9V/unsigned.json'))
        self.assertEqual(expected, actual)
