from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo4faM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo4faM(self):
        expected = get_data(
            path='operations/oo4faMeYmpYCpAydPp6e1orHeGzt6hHVezV8F6tLGXKgPuVk7is/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo4faMeYmpYCpAydPp6e1orHeGzt6hHVezV8F6tLGXKgPuVk7is/unsigned.json'))
        self.assertEqual(expected, actual)
