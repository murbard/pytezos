from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo1M5E(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo1M5E(self):
        expected = get_data(
            path='operations/oo1M5Ef25GGBAn7BF55zoRMTxG2zHX9bjhftwEDvzX5nJc6pFtu/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo1M5Ef25GGBAn7BF55zoRMTxG2zHX9bjhftwEDvzX5nJc6pFtu/unsigned.json'))
        self.assertEqual(expected, actual)
