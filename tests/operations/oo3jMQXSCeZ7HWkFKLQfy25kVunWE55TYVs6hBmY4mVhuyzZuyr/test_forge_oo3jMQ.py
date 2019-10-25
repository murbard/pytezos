from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3jMQ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3jMQ(self):
        expected = get_data(
            path='operations/oo3jMQXSCeZ7HWkFKLQfy25kVunWE55TYVs6hBmY4mVhuyzZuyr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3jMQXSCeZ7HWkFKLQfy25kVunWE55TYVs6hBmY4mVhuyzZuyr/unsigned.json'))
        self.assertEqual(expected, actual)
