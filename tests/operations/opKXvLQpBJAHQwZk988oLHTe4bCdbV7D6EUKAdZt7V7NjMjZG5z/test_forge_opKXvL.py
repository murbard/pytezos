from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKXvL(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKXvL(self):
        expected = get_data(
            path='operations/opKXvLQpBJAHQwZk988oLHTe4bCdbV7D6EUKAdZt7V7NjMjZG5z/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKXvLQpBJAHQwZk988oLHTe4bCdbV7D6EUKAdZt7V7NjMjZG5z/unsigned.json'))
        self.assertEqual(expected, actual)
