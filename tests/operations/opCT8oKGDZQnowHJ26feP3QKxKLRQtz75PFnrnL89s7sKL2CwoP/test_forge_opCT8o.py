from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopCT8o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opCT8o(self):
        expected = get_data(
            path='operations/opCT8oKGDZQnowHJ26feP3QKxKLRQtz75PFnrnL89s7sKL2CwoP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opCT8oKGDZQnowHJ26feP3QKxKLRQtz75PFnrnL89s7sKL2CwoP/unsigned.json'))
        self.assertEqual(expected, actual)
