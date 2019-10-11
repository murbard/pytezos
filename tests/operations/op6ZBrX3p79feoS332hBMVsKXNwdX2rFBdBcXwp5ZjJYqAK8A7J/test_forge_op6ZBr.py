from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop6ZBr(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op6ZBr(self):
        expected = get_data(
            path='operations/op6ZBrX3p79feoS332hBMVsKXNwdX2rFBdBcXwp5ZjJYqAK8A7J/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op6ZBrX3p79feoS332hBMVsKXNwdX2rFBdBcXwp5ZjJYqAK8A7J/unsigned.json'))
        self.assertEqual(expected, actual)
