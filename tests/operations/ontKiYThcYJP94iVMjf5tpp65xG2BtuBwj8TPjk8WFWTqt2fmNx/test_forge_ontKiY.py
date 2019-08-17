from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestontKiY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ontKiY(self):
        expected = get_data(
            path='operations/ontKiYThcYJP94iVMjf5tpp65xG2BtuBwj8TPjk8WFWTqt2fmNx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ontKiYThcYJP94iVMjf5tpp65xG2BtuBwj8TPjk8WFWTqt2fmNx/unsigned.json'))
        self.assertEqual(expected, actual)
