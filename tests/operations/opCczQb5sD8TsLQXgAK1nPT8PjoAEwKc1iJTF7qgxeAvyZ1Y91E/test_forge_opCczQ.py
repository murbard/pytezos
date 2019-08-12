from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopCczQ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opCczQ(self):
        expected = get_data(
            path='operations/opCczQb5sD8TsLQXgAK1nPT8PjoAEwKc1iJTF7qgxeAvyZ1Y91E/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opCczQb5sD8TsLQXgAK1nPT8PjoAEwKc1iJTF7qgxeAvyZ1Y91E/unsigned.json'))
        self.assertEqual(expected, actual)
