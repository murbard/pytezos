from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonr6ru(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onr6ru(self):
        expected = get_data(
            path='operations/onr6rubwGRGn2xYDfedFSfCDVeywgCzggMHvyVYP3GGppdYNmx4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onr6rubwGRGn2xYDfedFSfCDVeywgCzggMHvyVYP3GGppdYNmx4/unsigned.json'))
        self.assertEqual(expected, actual)
