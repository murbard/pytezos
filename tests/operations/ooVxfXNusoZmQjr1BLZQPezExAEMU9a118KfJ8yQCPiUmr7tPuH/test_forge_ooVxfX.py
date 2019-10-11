from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooVxfX(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooVxfX(self):
        expected = get_data(
            path='operations/ooVxfXNusoZmQjr1BLZQPezExAEMU9a118KfJ8yQCPiUmr7tPuH/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooVxfXNusoZmQjr1BLZQPezExAEMU9a118KfJ8yQCPiUmr7tPuH/unsigned.json'))
        self.assertEqual(expected, actual)
