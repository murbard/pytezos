from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop9kAY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op9kAY(self):
        expected = get_data(
            path='operations/op9kAYHDLWL8gZYStjMyGw3iBsGkqjmvx6VpyxLefonghXsN6LS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op9kAYHDLWL8gZYStjMyGw3iBsGkqjmvx6VpyxLefonghXsN6LS/unsigned.json'))
        self.assertEqual(expected, actual)
