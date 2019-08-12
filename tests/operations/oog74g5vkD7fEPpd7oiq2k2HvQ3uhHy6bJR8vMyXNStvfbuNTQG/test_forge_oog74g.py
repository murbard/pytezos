from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoog74g(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oog74g(self):
        expected = get_data(
            path='operations/oog74g5vkD7fEPpd7oiq2k2HvQ3uhHy6bJR8vMyXNStvfbuNTQG/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oog74g5vkD7fEPpd7oiq2k2HvQ3uhHy6bJR8vMyXNStvfbuNTQG/unsigned.json'))
        self.assertEqual(expected, actual)
