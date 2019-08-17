from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop9pWi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op9pWi(self):
        expected = get_data(
            path='operations/op9pWi2GKpY8jwFWbJk8pR9ztJXSvgySQz5w1cJRn2YSpShL9Uz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op9pWi2GKpY8jwFWbJk8pR9ztJXSvgySQz5w1cJRn2YSpShL9Uz/unsigned.json'))
        self.assertEqual(expected, actual)
