from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop2vts(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op2vts(self):
        expected = get_data(
            path='operations/op2vtsMH9WEgBjweK6GSym2LEQe6AD9oJmM9c3xUiaXDSHfxMfD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op2vtsMH9WEgBjweK6GSym2LEQe6AD9oJmM9c3xUiaXDSHfxMfD/unsigned.json'))
        self.assertEqual(expected, actual)
