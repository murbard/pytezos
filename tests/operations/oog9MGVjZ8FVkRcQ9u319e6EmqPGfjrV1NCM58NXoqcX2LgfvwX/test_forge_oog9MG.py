from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoog9MG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oog9MG(self):
        expected = get_data(
            path='operations/oog9MGVjZ8FVkRcQ9u319e6EmqPGfjrV1NCM58NXoqcX2LgfvwX/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oog9MGVjZ8FVkRcQ9u319e6EmqPGfjrV1NCM58NXoqcX2LgfvwX/unsigned.json'))
        self.assertEqual(expected, actual)
