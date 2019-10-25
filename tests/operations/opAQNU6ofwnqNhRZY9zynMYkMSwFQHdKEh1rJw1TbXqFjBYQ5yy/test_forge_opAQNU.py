from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopAQNU(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opAQNU(self):
        expected = get_data(
            path='operations/opAQNU6ofwnqNhRZY9zynMYkMSwFQHdKEh1rJw1TbXqFjBYQ5yy/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opAQNU6ofwnqNhRZY9zynMYkMSwFQHdKEh1rJw1TbXqFjBYQ5yy/unsigned.json'))
        self.assertEqual(expected, actual)
