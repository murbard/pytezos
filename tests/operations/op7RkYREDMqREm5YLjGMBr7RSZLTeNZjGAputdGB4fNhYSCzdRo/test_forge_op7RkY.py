from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop7RkY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op7RkY(self):
        expected = get_data(
            path='operations/op7RkYREDMqREm5YLjGMBr7RSZLTeNZjGAputdGB4fNhYSCzdRo/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op7RkYREDMqREm5YLjGMBr7RSZLTeNZjGAputdGB4fNhYSCzdRo/unsigned.json'))
        self.assertEqual(expected, actual)
