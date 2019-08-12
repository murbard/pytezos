from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooV7dR(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooV7dR(self):
        expected = get_data(
            path='operations/ooV7dR2yFF3g6KgaC6mjFhUWjbZWiui7qQLQsu1NAXG9rKz4HVM/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooV7dR2yFF3g6KgaC6mjFhUWjbZWiui7qQLQsu1NAXG9rKz4HVM/unsigned.json'))
        self.assertEqual(expected, actual)
